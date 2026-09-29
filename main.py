import tkinter as tk
from tkinter import messagebox
from auth import authenticate
from warehouse_window import open_warehouse_window
from personnel_window import open_personnel_window
from manager_window import open_manager_window
from boss_window import open_boss_window

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Авторизация - Northwind")
        self.root.geometry("300x200")
        
        tk.Label(self.root, text="Логин:").pack(pady=5)
        self.entry_login = tk.Entry(self.root)
        self.entry_login.pack(pady=5)
        
        tk.Label(self.root, text="Пароль:").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)
        
        tk.Button(self.root, text="Войти", command=self.login).pack(pady=20)
        
        self.root.mainloop()
    
    def login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()
        
        role = authenticate(login, password)
        
        if role:
            self.root.destroy()
            if role == 'warehouse':
                open_warehouse_window()
            elif role == 'personnel':
                open_personnel_window()
            elif role == 'manager':
                open_manager_window()
            elif role == 'boss':
                open_boss_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

if __name__ == "__main__":
    LoginApp()
