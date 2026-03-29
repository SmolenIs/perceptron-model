import tkinter as tk
from tkinter import ttk, messagebox
import logging

class PerceptronGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        
        # Налаштування головного вікна
        self.root.title("Моделювання ББП (Перцептрон)")
        self.root.geometry("550x450")
        
        # Читаємо колірну тему з config.json
        bg_color = "#333333" if config.get("theme") == "dark" else "#f0f0f0"
        fg_color = "white" if config.get("theme") == "dark" else "black"
        self.root.configure(bg=bg_color)
        
        # Налаштування стилів тексту
        style = ttk.Style()
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Arial", 10))
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)
        
        self.create_widgets()
        logging.info("Графічний інтерфейс ініціалізовано.")

    def create_widgets(self):
        # Блок (фрейм) для введення параметрів
        param_frame = ttk.LabelFrame(self.root, text="Параметри навчання ББП")
        param_frame.pack(padx=15, pady=15, fill="x")

        # Поле: Швидкість навчання
        ttk.Label(param_frame, text="Швидкість навчання (0.01 - 1.0):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.lr_entry = ttk.Entry(param_frame)
        self.lr_entry.insert(0, "0.1") # Значення за замовчуванням
        self.lr_entry.grid(row=0, column=1, padx=10, pady=10)

        # Поле: Кількість епох
        ttk.Label(param_frame, text="Кількість епох (напр. 5000):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.epochs_entry = ttk.Entry(param_frame)
        self.epochs_entry.insert(0, "5000")
        self.epochs_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Випадне меню: Логічна функція
        ttk.Label(param_frame, text="Логічна функція для моделювання:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.func_var = tk.StringVar(value="XOR")
        self.func_combo = ttk.Combobox(param_frame, textvariable=self.func_var, values=["AND", "OR", "XOR"], state="readonly")
        self.func_combo.grid(row=2, column=1, padx=10, pady=10)

        # Блок кнопок
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.train_btn = ttk.Button(btn_frame, text="Почати навчання", command=self.dummy_action)
        self.train_btn.grid(row=0, column=0, padx=10)

        self.report_btn = ttk.Button(btn_frame, text="Сформувати звіт", command=self.dummy_action)
        self.report_btn.grid(row=0, column=1, padx=10)

        # Текстове поле для виведення результатів та логів у самому вікні
        self.log_text = tk.Text(self.root, height=10, width=60, font=("Consolas", 10))
        self.log_text.pack(padx=15, pady=10)
        self.log_text.insert(tk.END, "Система готова до роботи. Введіть параметри та натисніть 'Почати навчання'.\n")
        self.log_text.config(state=tk.DISABLED) # Робимо поле тільки для читання

    def dummy_action(self):
        # Тимчасова заглушка для кнопок, поки ми не підключили логіку на Кроці 4
        messagebox.showinfo("Увага", "Ця функція буде підключена на наступному кроці (Крок 4)!")

# Блок для тестування (дозволяє запустити лише цей файл, щоб подивитися на вікно)
if __name__ == "__main__":
    root = tk.Tk()
    # Імітуємо конфіг для тесту
    app = PerceptronGUI(root, {"theme": "dark"}) 
    root.mainloop()