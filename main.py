import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

TOKEN = "7903728476:AAFzseQdua2iS8M-uugdTXa7OYmZt-ZFIFA"
ADMIN_ID = 207038530
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_clicks = {}  # Словарь для отслеживания кликов

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
    user_clicks[message.chat.id] = 0  # сбрасываем счётчик при старте

    description = (
        "Добро пожаловать в *FaucetUA!*\n\n"
        "Выберите интересующий ресурс и начните зарабатывать!"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("BtcViev", callback_data="link_clicked"),
        InlineKeyboardButton("FireFaucet", callback_data="link_clicked"),
        InlineKeyboardButton("Перейти на сайт FaucetUA", url="https://faucetua.online/")
    )

    bot.send_message(message.chat.id, description, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "link_clicked")
def handle_link_click(call):
    user_id = call.message.chat.id
    user_clicks[user_id] = user_clicks.get(user_id, 0) + 1

    if user_clicks[user_id] >= 2:
        bot.answer_callback_query(call.id, "Хочешь больше? Переходи на сайт!", show_alert=True)
        bot.send_message(user_id, "Хочешь больше? Переходи на сайт https://faucetua.online")
    else:
        bot.answer_callback_query(call.id, "Ссылка открыта.")

@bot.message_handler(commands=['sendall'])
def send_broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    text = message.text.replace('/sendall', '').strip()
    if not text:
        bot.reply_to(message, "Введите текст для рассылки.")
        return
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = [line.split('|')[0].strip() for line in f if line.strip()]
    except FileNotFoundError:
        users = []

    count = 0
    for user_id in users:
        try:
            bot.send_message(user_id, text)
            count += 1
        except:
            continue
    bot.reply_to(message, f"Сообщение отправлено {count} пользователям.")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        bot.reply_to(message, f"Пользователей в базе: {len(lines)}")
    except FileNotFoundError:
        bot.reply_to(message, "Файл пользователей не найден.")

# Запуск Flask в отдельном потоке
threading.Thread(target=run_flask).start()

print("Бот запущен...")
bot.infinity_polling()
