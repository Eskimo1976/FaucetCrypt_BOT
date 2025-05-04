import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

TOKEN = "7903728476:AAFzseQdua2iS8M-uugdTXa7OYmZt-ZFIFA"
ADMIN_ID = 207038530
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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

    description = (
        "Добро пожаловать в *FaucetUA!*\n\n"
        "Ниже представлены лучшие сайты для заработка криптовалюты без вложений.\n"
        "Выберите интересующий ресурс и начните зарабатывать!"
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
        ("FaucetPay", "https://faucetpay.io"),
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
        ("SkullBTC", "https://skullbtc.site"),
        ("SolWin", "https://solwin.site"),
        ("1doge", "https://1doge.site"),
        ("CFAIRDROP", "https://cfairdrop.site"),
        ("EarnEvery", "https://earnevery.site"),
        ("OnlyEarn", "https://onlyearn.site"),
        ("WheelPRO", "https://wheelpro.site"),
        ("USDTwins", "https://usdtwins.site"),
        # Ссылки со второй страницы сайта (home-1)
        ("BitcoFarm", "https://bitcofarm.online"),
        ("TopReward", "https://topreward.online"),
        ("CoinsFlow", "https://coinsflow.online"),
        ("LuckyClick", "https://luckyclick.online"),
        ("FaucetStep", "https://faucetstep.online"),
        ("DogeWin", "https://dogewin.online"),
        ("BTCCloud", "https://btccloud.online"),
        ("QuickCrypto", "https://quickcrypto.online"),
        ("DailySpin", "https://dailyspin.online"),
        ("MagicClaim", "https://magicclaim.online"),
        ("CryptoBox", "https://cryptobox.online"),
        ("AirClaim", "https://airclaim.online"),
        ("SpinGold", "https://spingold.online"),
        ("DigiMine", "https://digimine.online"),
        ("MoonClicks", "https://moonclicks.online"),
        ("LinkBits", "https://linkbits.online"),
    ]

    markup = InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(links), 2):
        row = [InlineKeyboardButton(text=name, url=url) for name, url in links[i:i + 2]]
        markup.add(*row)

    markup.add(InlineKeyboardButton("Перейти на сайт FaucetUA", url="https://faucetua.online/"))

    bot.send_message(message.chat.id, description, parse_mode="Markdown", reply_markup=markup)

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
