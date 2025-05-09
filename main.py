import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os
from dotenv import load_dotenv
from keep_alive import keep_alive  # Импорт поддержки активности

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 207038530
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_clicks = {}

@app.route("/")
def index():
    return "Бот работает!", 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

def save_user(user_id, username):
    with open(USERS_FILE, "a+", encoding="utf-8") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in [u.split("|")[0].strip() for u in users]:
            f.write(f"{user_id} | @{username or 'NoUsername'}\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id, message.from_user.username)
    user_clicks[message.chat.id] = 0

    description = (
        "Добро пожаловать в *FaucetBot!* \n"
        "Я помогу тебе находить лучшие краны для заработка криптовалюты. "
        "Просто выбери из меню ниже или жми на кнопки!"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Перейти на сайт", url="https://example.com")
    )

    bot.send_message(message.chat.id, description, parse_mode="Markdown", reply_markup=markup)

def polling_thread():
    bot.infinity_polling()

if __name__ == "__main__":
    keep_alive()  # Активируем поддержку постоянной работы (например, для Replit)
    threading.Thread(target=run_flask).start()
    polling_thread()
