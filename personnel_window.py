import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_config import get_connection

def open_personnel_window():
    root = tk.Tk()
    root.title("Отдел кадров - Northwind")
    root.geometry("900x500")
    
    columns = ('employee_id', 'last_name', 'first_name', 'title', 'city', 'country')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('employee_id', text='ID')
    tree.heading('last_name', text='Фамилия')
    tree.heading('first_name', text='Имя')
    tree.heading('title', text='Должность')
    tree.heading('city', text='Город')
    tree.heading('country', text='Страна')
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_employees():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT employee_id, last_name, first_name, title, city, country FROM employees ORDER BY employee_id")
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)
        cur.close()
        conn.close()
    
    def add_employee():
        last = simpledialog.askstring("Новый сотрудник", "Фамилия:")
        first = simpledialog.askstring("Новый сотрудник", "Имя:")
        if last and first:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COALESCE(MAX(employee_id), 0) + 1 FROM employees")
                new_id = cur.fetchone()[0]
                cur.execute("INSERT INTO employees (employee_id, last_name, first_name) VALUES (%s, %s, %s)",
                           (new_id, last, first))
                conn.commit()
                cur.close()
                conn.close()
                load_employees()
                messagebox.showinfo("Успех", f"Сотрудник '{last} {first}' добавлен с ID={new_id}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def edit_employee():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сотрудника")
            return
        values = tree.item(selected[0])['values']
        emp_id = values[0]
        
        new_title = simpledialog.askstring("Редактирование", "Новая должность:", initialvalue=values[3])
        new_city = simpledialog.askstring("Редактирование", "Новый город:", initialvalue=values[4])
        new_country = simpledialog.askstring("Редактирование", "Новая страна:", initialvalue=values[5])
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE employees SET title = %s, city = %s, country = %s WHERE employee_id = %s",
                       (new_title, new_city, new_country, emp_id))
            conn.commit()
            cur.close()
            conn.close()
            load_employees()
            messagebox.showinfo("Успех", "Данные сотрудника обновлены")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def delete_employee():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сотрудника")
            return
        values = tree.item(selected[0])['values']
        emp_id = values[0]
        emp_name = f"{values[1]} {values[2]}"
        
        if messagebox.askyesno("Удаление", f"Удалить сотрудника '{emp_name}'?"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE orders SET employee_id = NULL WHERE employee_id = %s", (emp_id,))
                cur.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
                conn.commit()
                cur.close()
                conn.close()
                load_employees()
                messagebox.showinfo("Успех", "Сотрудник удален")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Добавить", command=add_employee).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Редактировать", command=edit_employee).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Удалить", command=delete_employee).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Обновить", command=load_employees).pack(side='left', padx=5)
    
    load_employees()
    root.mainloop()
