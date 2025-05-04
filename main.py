import telebot
import os
from keep_alive import keep_alive  # Flask-сервер для UptimeRobot

TOKEN = "ТВОЙ_ТОКЕН"
ADMIN_ID = 2070385303  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)
USERS_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write(str(user_id) + "\n")
        return
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    save_user(user_id)

    description = (
        "Добро пожаловать в крипто-бот!\n\n"
        "Здесь вы найдёте лучшие сайты для заработка криптовалюты. "
        "Выбирайте нужный сайт и начинайте зарабатывать!"
    )

    links = [
        ("OnlyFaucet — простой кран", "https://onlyfaucet.com"),
        ("EarnCryptoWRS — бонусы", "https://earncryptowrs.in"),
        ("Gamerlee — игры и крипта", "https://gamerlee.com"),
        ("EarnSolana — кран Solana", "https://earnsolana.xyz"),
        ("CryptoFuture — задания", "https://cryptofuture.co.in"),
        ("ClaimCrypto — быстрые выплаты", "https://claimcrypto.in"),
        ("EftaCrypto — простой интерфейс", "https://eftacrypto.com"),
        ("FreeLTC — Litecoin кран", "https://freeltc.fun"),
        ("Wheel of Gold — крутите колесо", "https://wheelofgold.com"),
        ("FaucetWorld — много кранов", "https://faucetworld.in"),
        ("RS Faucet — TRX и другие", "https://rsfaucet.com"),
        ("BestPayingFaucet — ТОП сайты", "https://bestpayingfaucet.online"),
        ("Earn Pepe — заработок на PEPE", "https://earn-pepe.com"),
        ("EarnTrump — крипто-Трамп", "https://earn-trump.com"),
        ("BagiCoin — быстрая регистрация", "https://bagi.co.in"),
        ("FaucetPay кошелек", "https://faucetpay.io"),
        ("SatoshiFaucet — классика", "https://satoshifaucet.io"),
        ("AdBTC — серфинг за BTC", "https://r.adbtc.top"),
        ("TON Links", "https://ton.leaks.work"),
        ("Kiddy Earner", "https://kiddyearner.com"),
        ("USDT Faucet", "https://treaw.com"),
        ("Dogecoin Link", "https://ch3zo.com"),
        ("FaucetPayz", "https://faucetpayz.com"),
        ("Whoopy Rewards", "https://whoopyrewards.com"),
        ("Genki Miner", "https://genkiminer.com"),
        ("Assetni — мульти-кран", "https://assetni.com"),
    ]

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(links), 2):
        buttons = [telebot.types.InlineKeyboardButton(name, url=url) for name, url in links[i:i+2]]
        markup.add(*buttons)

    bot.send_message(user_id, description, reply_markup=markup)

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
        users = f.read().splitlines()

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
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            count = len(f.read().splitlines())
    else:
        count = 0
    bot.reply_to(message, f"Количество пользователей: {count}")

keep_alive()
bot.infinity_polling()
