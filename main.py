import json
import logging
import os
import sys
from gui import ModernPerceptronApp

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Критична помилка: Файл {config_path} не знайдено. Використовуються стандартні налаштування.")
        return {"log_file": "app.log", "theme": "dark", "reports_dir": "./reports"}

config = load_config()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.get("log_file", "perceptron_app.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

reports_dir = config.get("reports_dir", "./reports")
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
    logging.info(f"Створено директорію для звітів: {reports_dir}")

logging.info(f"Програму запущено. Версія: {config.get('app_version', 'невідома')}")

if __name__ == "__main__":
    logging.info("Базове налаштування успішно завершено. Запуск GUI...")
    # Запускаємо сучасний додаток
    app = ModernPerceptronApp(config)
    app.mainloop()
    