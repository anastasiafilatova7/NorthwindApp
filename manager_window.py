import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_config import get_connection

def open_manager_window():
    root = tk.Tk()
    root.title("Менеджер - Northwind")
    root.geometry("1100x650")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    #ЗАКАЗЫ
    orders_frame = ttk.Frame(notebook)
    notebook.add(orders_frame, text="Заказы")
    
    order_columns = ('order_id', 'customer_id', 'order_date', 'shipped_date', 'ship_country')
    order_tree = ttk.Treeview(orders_frame, columns=order_columns, show='headings')
    order_tree.heading('order_id', text='ID заказа')
    order_tree.heading('customer_id', text='Клиент')
    order_tree.heading('order_date', text='Дата заказа')
    order_tree.heading('shipped_date', text='Дата отгрузки')
    order_tree.heading('ship_country', text='Страна')
    order_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_orders():
        for row in order_tree.get_children():
            order_tree.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT order_id, customer_id, order_date, shipped_date, ship_country FROM orders ORDER BY order_id DESC LIMIT 100")
        for row in cur.fetchall():
            order_tree.insert('', 'end', values=row)
        cur.close()
        conn.close()
    
    def add_order():
        cust_id = simpledialog.askstring("Новый заказ", "ID клиента (например, VINET):")
        if cust_id:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT customer_id FROM customers WHERE customer_id = %s", (cust_id,))
                if not cur.fetchone():
                    messagebox.showerror("Ошибка", f"Клиент с ID '{cust_id}' не найден!")
                    cur.close()
                    conn.close()
                    return
                
                cur.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders")
                new_order_id = cur.fetchone()[0]
                
                cur.execute("INSERT INTO orders (order_id, customer_id, order_date) VALUES (%s, %s, CURRENT_DATE)",
                           (new_order_id, cust_id))
                conn.commit()
                cur.close()
                conn.close()
                load_orders()
                messagebox.showinfo("Успех", f"Заказ №{new_order_id} создан для клиента {cust_id}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def edit_order():
        selected = order_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return
        values = order_tree.item(selected[0])['values']
        order_id = values[0]
        
        new_country = simpledialog.askstring("Редактирование", "Новая страна доставки:", initialvalue=values[4])
        if new_country:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE orders SET ship_country = %s WHERE order_id = %s", (new_country, order_id))
                conn.commit()
                cur.close()
                conn.close()
                load_orders()
                messagebox.showinfo("Успех", "Заказ обновлен")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def delete_order():
        selected = order_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return
        values = order_tree.item(selected[0])['values']
        order_id = values[0]
        
        if messagebox.askyesno("Удаление", f"Удалить заказ №{order_id}?\n(Будут удалены и детали заказа)"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))
                cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                conn.commit()
                cur.close()
                conn.close()
                load_orders()
                messagebox.showinfo("Успех", "Заказ удален")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    order_btn_frame = ttk.Frame(orders_frame)
    order_btn_frame.pack(pady=10)
    ttk.Button(order_btn_frame, text="Добавить заказ", command=add_order).pack(side='left', padx=5)
    ttk.Button(order_btn_frame, text="Редактировать", command=edit_order).pack(side='left', padx=5)
    ttk.Button(order_btn_frame, text="Удалить заказ", command=delete_order).pack(side='left', padx=5)
    ttk.Button(order_btn_frame, text="Обновить", command=load_orders).pack(side='left', padx=5)
    
    load_orders()
    
    #КЛИЕНТЫ
    customers_frame = ttk.Frame(notebook)
    notebook.add(customers_frame, text="Клиенты")
    
    cust_columns = ('customer_id', 'company_name', 'contact_name', 'city', 'country')
    cust_tree = ttk.Treeview(customers_frame, columns=cust_columns, show='headings')
    cust_tree.heading('customer_id', text='ID')
    cust_tree.heading('company_name', text='Компания')
    cust_tree.heading('contact_name', text='Контакт')
    cust_tree.heading('city', text='Город')
    cust_tree.heading('country', text='Страна')
    cust_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_customers():
        for row in cust_tree.get_children():
            cust_tree.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT customer_id, company_name, contact_name, city, country FROM customers ORDER BY customer_id")
        for row in cur.fetchall():
            cust_tree.insert('', 'end', values=row)
        cur.close()
        conn.close()
    
    def add_customer():
        cust_id = simpledialog.askstring("Новый клиент", "ID клиента (5 букв, например, ABCDE):")
        if not cust_id:
            return
        if len(cust_id) > 5:
            messagebox.showerror("Ошибка", "ID клиента должен быть не более 5 символов")
            return
        
        name = simpledialog.askstring("Новый клиент", "Название компании:")
        if not name:
            return
        
        contact = simpledialog.askstring("Новый клиент", "Контактное лицо (можно оставить пустым):")
        city = simpledialog.askstring("Новый клиент", "Город (можно оставить пустым):")
        country = simpledialog.askstring("Новый клиент", "Страна (можно оставить пустым):")
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO customers (customer_id, company_name, contact_name, city, country) 
                VALUES (%s, %s, %s, %s, %s)
            """, (cust_id, name, contact, city, country))
            conn.commit()
            cur.close()
            conn.close()
            load_customers()
            messagebox.showinfo("Успех", f"Клиент '{name}' добавлен с ID={cust_id}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента:\n{e}")
    
    def edit_customer():
        selected = cust_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите клиента")
            return
        values = cust_tree.item(selected[0])['values']
        cust_id = values[0]
        
        new_name = simpledialog.askstring("Редактирование", "Название компании:", initialvalue=values[1])
        new_contact = simpledialog.askstring("Редактирование", "Контактное лицо:", initialvalue=values[2])
        
        if new_name:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE customers SET company_name = %s, contact_name = %s WHERE customer_id = %s",
                           (new_name, new_contact, cust_id))
                conn.commit()
                cur.close()
                conn.close()
                load_customers()
                messagebox.showinfo("Успех", "Клиент обновлен")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def delete_customer():
        selected = cust_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите клиента")
            return
        values = cust_tree.item(selected[0])['values']
        cust_id = values[0]
        cust_name = values[1]
        
        if messagebox.askyesno("Удаление", f"Удалить клиента '{cust_name}'?\n(Будут удалены и его заказы)"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM order_details WHERE order_id IN (SELECT order_id FROM orders WHERE customer_id = %s)", (cust_id,))
                cur.execute("DELETE FROM orders WHERE customer_id = %s", (cust_id,))
                cur.execute("DELETE FROM customers WHERE customer_id = %s", (cust_id,))
                conn.commit()
                cur.close()
                conn.close()
                load_customers()
                messagebox.showinfo("Успех", "Клиент удален")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    cust_btn_frame = ttk.Frame(customers_frame)
    cust_btn_frame.pack(pady=10)
    ttk.Button(cust_btn_frame, text="Добавить клиента", command=add_customer).pack(side='left', padx=5)
    ttk.Button(cust_btn_frame, text="Редактировать", command=edit_customer).pack(side='left', padx=5)
    ttk.Button(cust_btn_frame, text="Удалить клиента", command=delete_customer).pack(side='left', padx=5)
    ttk.Button(cust_btn_frame, text="Обновить", command=load_customers).pack(side='left', padx=5)
    
    load_customers()
    
    root.mainloop()
