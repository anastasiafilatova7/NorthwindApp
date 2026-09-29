import tkinter as tk
from tkinter import ttk
from db_config import get_connection

def open_boss_window():
    root = tk.Tk()
    root.title("Начальник - Отчеты Northwind")
    root.geometry("900x600")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    #ОТЧЕТ ПО КЛИЕНТАМ
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="Отчет по клиентам")
    
    columns1 = ('company_name', 'orders_count')
    tree1 = ttk.Treeview(frame1, columns=columns1, show='headings')
    tree1.heading('company_name', text='Клиент')
    tree1.heading('orders_count', text='Количество заказов')
    tree1.pack(fill='both', expand=True, padx=10, pady=10)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.company_name, COUNT(o.order_id) as orders_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.company_name
        ORDER BY orders_count DESC
    """)
    for row in cur.fetchall():
        tree1.insert('', 'end', values=row)
    cur.close()
    conn.close()
    
    #ОТЧЕТ ПО СОТРУДНИКАМ
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="Отчет по сотрудникам")
    
    columns2 = ('last_name', 'first_name', 'orders_count')
    tree2 = ttk.Treeview(frame2, columns=columns2, show='headings')
    tree2.heading('last_name', text='Фамилия')
    tree2.heading('first_name', text='Имя')
    tree2.heading('orders_count', text='Количество заказов')
    tree2.pack(fill='both', expand=True, padx=10, pady=10)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.last_name, e.first_name, COUNT(o.order_id) as orders_count
        FROM employees e
        LEFT JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id, e.last_name, e.first_name
        ORDER BY orders_count DESC
    """)
    for row in cur.fetchall():
        tree2.insert('', 'end', values=row)
    cur.close()
    conn.close()
    
    #ОТЧЕТ ПО КАТЕГОРИЯМ
    frame3 = ttk.Frame(notebook)
    notebook.add(frame3, text="Отчет по категориям")
    
    columns3 = ('category_name', 'products_count', 'avg_price')
    tree3 = ttk.Treeview(frame3, columns=columns3, show='headings')
    tree3.heading('category_name', text='Категория')
    tree3.heading('products_count', text='Кол-во продуктов')
    tree3.heading('avg_price', text='Средняя цена')
    tree3.pack(fill='both', expand=True, padx=10, pady=10)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.category_name, COUNT(p.product_id) as products_count, AVG(p.unit_price) as avg_price
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY products_count DESC
    """)
    for row in cur.fetchall():
        tree3.insert('', 'end', values=row)
    cur.close()
    conn.close()
    
    root.mainloop()
