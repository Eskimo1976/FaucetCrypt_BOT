from flask import Flask
import threading
import os

# Создаём Flask-приложение
app = Flask(__name__)

# Обрабатываем корневой маршрут
@app.route('/')
def home():
    return 'Бот работает!'

# Функция запуска Flask-сервера
def run():
    port = int(os.environ.get('PORT', 3000))  # Railway передаёт нужный порт сюда
    app.run(host='0.0.0.0', port=port)

# Фоновый запуск сервера
def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
