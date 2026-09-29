import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_config import get_connection

def open_warehouse_window():
    root = tk.Tk()
    root.title("Работник склада - Northwind")
    root.geometry("1000x650")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    #ПРОДУКТЫ
    products_frame = ttk.Frame(notebook)
    notebook.add(products_frame, text="Продукты")
    
    columns = ('product_id', 'product_name', 'unit_price', 'units_in_stock')
    tree = ttk.Treeview(products_frame, columns=columns, show='headings')
    tree.heading('product_id', text='ID')
    tree.heading('product_name', text='Название')
    tree.heading('unit_price', text='Цена')
    tree.heading('units_in_stock', text='На складе')
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_products():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT product_id, product_name, unit_price, units_in_stock FROM products ORDER BY product_id")
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)
        cur.close()
        conn.close()
    
    def add_product():
        name = simpledialog.askstring("Новый продукт", "Название продукта:")
        if name:
            price = simpledialog.askfloat("Новый продукт", "Цена:")
            stock = simpledialog.askinteger("Новый продукт", "Количество на складе:")
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO products (product_name, unit_price, units_in_stock, discontinued) VALUES (%s, %s, %s, 0)",
                       (name, price, stock))
            conn.commit()
            cur.close()
            conn.close()
            load_products()
            messagebox.showinfo("Успех", "Продукт добавлен")
    
    def edit_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите продукт")
            return
        values = tree.item(selected[0])['values']
        product_id = values[0]
        new_price = simpledialog.askfloat("Редактирование", "Новая цена:", initialvalue=values[2])
        new_stock = simpledialog.askinteger("Редактирование", "Новое количество:", initialvalue=values[3])
        if new_price and new_stock:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE products SET unit_price = %s, units_in_stock = %s WHERE product_id = %s",
                       (new_price, new_stock, product_id))
            conn.commit()
            cur.close()
            conn.close()
            load_products()
            messagebox.showinfo("Успех", "Продукт обновлен")
    
    def delete_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите продукт")
            return
        if messagebox.askyesno("Удаление", "Удалить выбранный продукт?"):
            product_id = tree.item(selected[0])['values'][0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            conn.commit()
            cur.close()
            conn.close()
            load_products()
    
    btn_frame = ttk.Frame(products_frame)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Добавить", command=add_product).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Редактировать", command=edit_product).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Удалить", command=delete_product).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Обновить", command=load_products).pack(side='left', padx=5)
    
    load_products()
    
    #КАТЕГОРИИ
    categories_frame = ttk.Frame(notebook)
    notebook.add(categories_frame, text="Категории")
    
    cat_columns = ('category_id', 'category_name', 'description')
    cat_tree = ttk.Treeview(categories_frame, columns=cat_columns, show='headings')
    cat_tree.heading('category_id', text='ID')
    cat_tree.heading('category_name', text='Название')
    cat_tree.heading('description', text='Описание')
    cat_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_categories():
        for row in cat_tree.get_children():
            cat_tree.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT category_id, category_name, description FROM categories ORDER BY category_id")
        for row in cur.fetchall():
            cat_tree.insert('', 'end', values=row)
        cur.close()
        conn.close()
    
    def add_category():
        name = simpledialog.askstring("Новая категория", "Название категории:")
        if name:
            desc = simpledialog.askstring("Новая категория", "Описание категории (можно оставить пустым):")
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM categories")
                new_id = cur.fetchone()[0]
                if desc:
                    cur.execute("INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)",
                               (new_id, name, desc))
                else:
                    cur.execute("INSERT INTO categories (category_id, category_name) VALUES (%s, %s)",
                               (new_id, name))
                conn.commit()
                cur.close()
                conn.close()
                load_categories()
                messagebox.showinfo("Успех", f"Категория '{name}' добавлена (ID={new_id})")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def delete_category():
        selected = cat_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return
        if messagebox.askyesno("Удаление", "Удалить выбранную категорию?"):
            category_id = cat_tree.item(selected[0])['values'][0]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE products SET category_id = NULL WHERE category_id = %s", (category_id,))
                cur.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
                conn.commit()
                cur.close()
                conn.close()
                load_categories()
                messagebox.showinfo("Успех", "Категория удалена")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    cat_btn_frame = ttk.Frame(categories_frame)
    cat_btn_frame.pack(pady=10)
    ttk.Button(cat_btn_frame, text="Добавить", command=add_category).pack(side='left', padx=5)
    ttk.Button(cat_btn_frame, text="Удалить", command=delete_category).pack(side='left', padx=5)
    ttk.Button(cat_btn_frame, text="Обновить", command=load_categories).pack(side='left', padx=5)
    
    load_categories()
    
    root.mainloop()
