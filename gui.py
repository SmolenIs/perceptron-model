import customtkinter as ctk
import logging
import numpy as np
import os
from datetime import datetime
from perceptron import MultilayerBinaryPerceptron
import tkinter.messagebox as messagebox

class ModernPerceptronApp(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        # Налаштування вікна
        self.title("Моделювання ББП (Перцептрон)")
        self.geometry("650x600")
        
        # Встановлюємо тему з конфігу (dark або light)
        ctk.set_appearance_mode(self.config.get("theme", "dark"))
        ctk.set_default_color_theme("blue")
        
        self.last_results = "" # Змінна для зберігання результатів для звіту
        
        self.create_widgets()
        logging.info("Сучасний графічний інтерфейс ініціалізовано.")

    def create_widgets(self):
        # Головний фрейм
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Налаштування нейромережі", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Фрейм для параметрів
        self.params_frame = ctk.CTkFrame(self.main_frame)
        self.params_frame.pack(pady=10, padx=20, fill="x")

        # Швидкість навчання
        self.lr_label = ctk.CTkLabel(self.params_frame, text="Швидкість навчання:")
        self.lr_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.lr_entry = ctk.CTkEntry(self.params_frame, placeholder_text="0.1")
        self.lr_entry.insert(0, "0.1")
        self.lr_entry.grid(row=0, column=1, padx=20, pady=10)

        # Епохи
        self.epochs_label = ctk.CTkLabel(self.params_frame, text="Кількість епох:")
        self.epochs_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.epochs_entry = ctk.CTkEntry(self.params_frame, placeholder_text="5000")
        self.epochs_entry.insert(0, "5000")
        self.epochs_entry.grid(row=1, column=1, padx=20, pady=10)

        # Логічна функція
        self.func_label = ctk.CTkLabel(self.params_frame, text="Логічна функція:")
        self.func_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.func_combo = ctk.CTkComboBox(self.params_frame, values=["AND", "OR", "XOR"])
        self.func_combo.set("XOR")
        self.func_combo.grid(row=2, column=1, padx=20, pady=10)

        # Кнопки
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.train_btn = ctk.CTkButton(self.btn_frame, text="Почати навчання", command=self.start_training)
        self.train_btn.pack(side="left", padx=10)

        self.report_btn = ctk.CTkButton(self.btn_frame, text="Зберегти звіт", command=self.save_report)
        self.report_btn.pack(side="left", padx=10)

        # Текстове поле для логів
        self.log_textbox = ctk.CTkTextbox(self.main_frame, width=500, height=200)
        self.log_textbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_textbox.insert("0.0", "Готово до роботи. Введіть параметри та натисніть 'Почати навчання'.\n")

    def print_to_log(self, text):
        """Додає текст у вікно результатів"""
        self.log_textbox.insert("end", text + "\n")
        self.log_textbox.see("end")

    def start_training(self):
        """Обробка натискання кнопки навчання та валідація даних"""
        self.log_textbox.delete("0.0", "end") # Очищуємо поле
        
        # 1. Валідація введення (обробка некоректних даних)
        try:
            lr = float(self.lr_entry.get())
            epochs = int(self.epochs_entry.get())
            if lr <= 0 or epochs <= 0:
                raise ValueError("Значення мають бути більше нуля.")
        except ValueError as e:
            error_msg = f"Помилка введення: Будь ласка, введіть коректні числа. Деталі: {e}"
            logging.error(error_msg)
            messagebox.showerror("Помилка", error_msg)
            self.print_to_log("❌ " + error_msg)
            return

        func_type = self.func_combo.get()
        self.print_to_log(f"🔄 Починаємо навчання для функції {func_type}...\nЕпох: {epochs}, Швидкість: {lr}")
        
        # 2. Підготовка даних (таблиці істинності)
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        if func_type == "AND":
            y = np.array([[0], [0], [0], [1]])
        elif func_type == "OR":
            y = np.array([[0], [1], [1], [1]])
        else: # XOR
            y = np.array([[0], [1], [1], [0]])

        # 3. Навчання перцептрона
        try:
            mlp = MultilayerBinaryPerceptron(learning_rate=lr)
            mlp.train(X, y, epochs)
            
            # 4. Тестування та виведення результатів
            self.print_to_log("\n✅ Навчання завершено! Результати тестування:")
            predictions = mlp.predict(X)
            
            result_text = f"Звіт моделювання ({func_type}):\n"
            result_text += f"Параметри: Епохи={epochs}, LR={lr}\n"
            result_text += "-"*30 + "\n"
            for i in range(len(X)):
                res = f"Вхід: {X[i]} -> Очікувано: {y[i][0]} | Отримано: {predictions[i][0]}"
                self.print_to_log(res)
                result_text += res + "\n"
            
            self.last_results = result_text # Зберігаємо для звіту
            
        except Exception as e:
            logging.error(f"Критична помилка під час навчання: {e}")
            self.print_to_log(f"❌ Сталася помилка: {e}")

    def save_report(self):
        """Формування результатів у файл"""
        if not self.last_results:
            messagebox.showwarning("Увага", "Спочатку проведіть навчання, щоб сформувати звіт.")
            return
            
        reports_dir = self.config.get("reports_dir", "./reports")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{self.func_combo.get()}_{timestamp}.txt"
        filepath = os.path.join(reports_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.last_results)
            logging.info(f"Звіт збережено: {filepath}")
            self.print_to_log(f"\n💾 Звіт успішно збережено у файл:\n{filepath}")
            messagebox.showinfo("Успіх", f"Звіт збережено: {filename}")
        except Exception as e:
            logging.error(f"Помилка збереження звіту: {e}")
            self.print_to_log(f"\n❌ Помилка збереження звіту: {e}")