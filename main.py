import telebot
import os
from keep_alive import keep_alive  # Flask-сервер для UptimeRobot

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))

if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")

bot = telebot.TeleBot(TOKEN)
USERS_FILE = "users.txt"

# Сохраняем пользователя
def save_user(user_id, username):
    new_entry = f"{user_id} | @{username or 'Без_ника'}"
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write(new_entry + "\n")
        return
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if not any(str(user_id) in u for u in users):
        with open(USERS_FILE, "a") as f:
            f.write(new_entry + "\n")

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id, message.from_user.username)

    description = (
        "Привет! Это бот сайта [FaucetUA](https://faucetua.online/) — сборник лучших кранов, "
        "позволяющих зарабатывать криптовалюту бесплатно. Просто выбери любой сайт из списка ниже и начинай зарабатывать!"
    )

    links = [
        ("BtcViev", "https://www.bitcoviews.com"),
        ("FireFaucet", "https://firefaucet.win"),
        ("Moneta FV", "https://helpfpcoin.site"),
        ("OnlyFaucet", "https://onlyfaucet.com"),
        ("СrYpto", "https://earncryptowrs.in"),
        ("Gemerle", "https://gamerlee.com"),
        ("EarnSolana", "https://earnsolana.xyz"),
        ("CryptoFuture", "https://cryptofuture.co.in"),
        ("ClaimCrypt", "https://claimcrypto.in"),
        ("Effa Crypt", "https://eftacrypto.com"),
        ("Freee Crypto", "https://freeltc.fun"),
        ("Wheal", "https://wheelofgold.com"),
        ("FaucetWorld", "https://faucetworld.in"),
        ("RS Faucet", "https://rsfaucet.com"),
        ("BestPaying", "https://bestpayingfaucet.online"),
        ("Earn Crypto", "https://earn-pepe.com"),
        ("EarnTrump", "https://earn-trump.com"),
        ("Baggy Cript", "https://bagi.co.in"),
        ("FaucetPay", "https://faucetpay.io"),
        ("SatoshiFaucet", "https://satoshifaucet.io"),
        ("Ad BTC", "https://r.adbtc.top"),
        ("Links TON", "https://ton.leaks.work"),
        ("KiddyEarn", "https://kiddyearner.com"),
        ("FaucetUsdt", "https://treaw.com"),
        ("Link Dogy", "https://ch3zo.com"),
        ("FaucetPayz", "https://faucetpayz.com"),
        ("Whoopyy", "https://whoopyrewards.com"),
        ("GenkyMinner", "https://genkiminer.com"),
        ("MultiCoin", "https://assetni.com"),
    ]

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(links), 2):
        buttons = [telebot.types.InlineKeyboardButton(name, url=url) for name, url in links[i:i+2]]
        markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        description,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=markup
    )

# Команда /sendall — рассылка от администратора
@bot.message_handler(commands=['sendall'])
def send_broadcast(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")
        return

    text = message.text.replace('/sendall', '').strip()
    if not text:
        bot.reply_to(message, "Укажите текст для рассылки.")
        return

    if not os.path.exists(USERS_FILE):
        bot.reply_to(message, "Нет пользователей для рассылки.")
        return

    with open(USERS_FILE, "r") as f:
        user_lines = f.read().splitlines()

    count = 0
    for line in user_lines:
        user_id = line.split("|")[0].strip()
        try:
            bot.send_message(user_id, text)
            count += 1
        except:
            continue
    bot.reply_to(message, f"Сообщение отправлено {count} пользователям.")

# Команда /stats — статистика пользователей
@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.chat.id != ADMIN_ID:
        return
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
            count = len(users)
    else:
        count = 0
    bot.reply_to(message, f"Всего пользователей: {count}")

# Запуск
keep_alive()
bot.infinity_polling()
