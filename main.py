import telebot
import os
from keep_alive import keep_alive  # Flask-сервер для UptimeRobot

# Получаем токен из переменной окружения
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(telebot.types.InlineKeyboardButton("Перейти на FaucetUA", url="https://faucetua.online/"))

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

    for i in range(0, len(links), 2):
        buttons = [telebot.types.InlineKeyboardButton(name, url=url) for name, url in links[i:i+2]]
        markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите сайт для заработка криптовалюты:",
        reply_markup=markup
    )

# Запускаем фоновый Flask-сервер
keep_alive()

# Запускаем Telegram-бота
bot.infinity_polling()