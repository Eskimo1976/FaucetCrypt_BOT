import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7903728476:AAFzseQdua2iS8M-uugdTXa7OYmZt-ZFIFA"
ADMIN_ID = 2070385303
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)

# Сохраняет ID пользователя
def save_user(user_id, username):
    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id} | @{username}\n")

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id, message.from_user.username or "NoUsername")

    description = (
        "Добро пожаловать в бота *FaucetUA!* Здесь собраны сайты, на которых можно заработать криптовалюту."
        "\n\nНажмите на любую кнопку ниже, чтобы перейти на сайт."
    )

    links = [
        ("BtcViev", "https://www.bitcoviews.com"),
        ("FireFaucet", "https://firefaucet.win"),
        ("Moneta FV", "https://helpfpcoin.site"),
        ("Link LTC", "https://cflink.pw"),
        ("Link USDT", "https://cflink.pw"),
        ("Dogycoin", "https://cflink.pw"),
        ("Binance", "https://cflink.pw"),
        ("PEPE", "https://cflink.pw"),
        ("SolanaCF", "https://cflink.pw"),
        ("ADTrump", "https://cflink.pw"),
        ("Links TRX", "https://cflink.pw"),
        ("LINKS TaRa", "https://cflink.pw"),
        ("CF Ripple", "https://cflink.pw"),
        ("Poligon", "https://cflink.pw"),
        ("OnlyFaucet", "https://onlyfaucet.com"),
        ("СrYpto", "https://earncryptowrs.in"),
        ("Gemerle", "https://gamerlee.com"),
        ("EarnSolana", "https://earnsolana.xyz"),
        ("CryptoFuture", "https://cryptofuture.co.in"),
        ("ClaimCrypt", "https://claimcrypto.in"),
        ("Effa Crypt", "https://eftacrypto.com"),
        ("Freee Crypt", "https://freeltc.fun"),
        ("Wheal", "https://wheelofgold.com"),
        ("FaucetWorld", "https://faucetworld.in"),
        ("RS Faucet", "https://rsfaucet.com"),
        ("BestPaying", "https://bestpayingfaucet.online"),
        ("Earn Crypto", "https://earn-pepe.com"),
        ("EarnTrump", "https://earn-trump.com"),
        ("Baggy Cript", "https://bagi.co.in"),
        ("Кошелек FaucetPay", "https://faucetpay.io"),
        ("SatoshiFau", "https://satoshifaucet.io"),
        ("Ad BTC", "https://r.adbtc.top"),
        ("Links TON", "https://ton.leaks.work"),
        ("KiddyEarn", "https://kiddyearner.com"),
        ("FaucetUsdt", "https://treaw.com"),
        ("Link Dogy", "https://ch3zo.com"),
        ("FaucetPayz", "https://faucetpayz.com"),
        ("Whoopyy", "https://whoopyrewards.com"),
        ("GenkMinner", "https://genkiminer.com"),
        ("MultiCoin", "https://assetni.com"),
    ]

    markup = InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(links), 2):
        row = [InlineKeyboardButton(text=links[j][0], url=links[j][1]) for j in range(i, min(i+2, len(links)))]
        markup.add(*row)

    bot.send_message(message.chat.id, description, parse_mode="Markdown", reply_markup=markup)

# Команда /sendall для рассылки
@bot.message_handler(commands=['sendall'])
def send_broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    text = message.text.replace('/sendall', '').strip()
    if not text:
        bot.reply_to(message, "Введите текст для рассылки.")
        return

    try:
        with open(USERS_FILE, "r") as f:
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

# Команда /stats
@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
        bot.reply_to(message, f"Пользователей в базе: {len(lines)}")
    except FileNotFoundError:
        bot.reply_to(message, "Файл пользователей не найден.")

print("Бот запущен...")
bot.infinity_polling()
