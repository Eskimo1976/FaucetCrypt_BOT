import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("TOKEN")
USERS_FILE = "users.txt"
ADMIN_ID = 207038530

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
user_states = {}

@app.route("/")
def index():
    return "Бот работает!", 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# ДОБАВЛЕНО: безопасное создание users.txt
def save_user(user_id, username):
    os.makedirs(os.path.dirname(USERS_FILE) or ".", exist_ok=True)
    with open(USERS_FILE, "a+", encoding="utf-8") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in [u.split("|")[0].strip() for u in users]:
            f.write(f"{user_id} | @{username or 'NoUsername'}\n")

# Категории ссылок
categories = {
    "Перспективные": [
        ("EarnSolana", "https://earnsolana.xyz/?r=14425"),
        ("EarnBonk", "https://earn-bonk.com/?ref=dCwrb"),
        ("FreePepe", "https://free-pepe.com/?r=110592"),
        ("ClaimFlora", "https://claimflora.com/?r=563"),
        ("EFTA Crypto", "https://eftacrypto.com/claim/tron/?r=karamba1199@gmail.com")
    ],
    "Мультикраны": [
        ("FireFaucet", "https://firefaucet.win/ref/Beriya1985"),
        ("FaucetCrypto", "https://faucetcrypto.net/?r=86978"),
        ("AutoFaucet", "https://autofaucet.dutchycorp.space/?r=Beriya"),
        ("ClaimCrypto", "https://claimcrypto.in/?r=1728"),
        ("CH3ZO", "https://ch3zo.com/?r=DBBDukPiMV1VsXL1BUPBd5cjtTVJx3uo8P"),
        ("SimpleBits", "https://simplebits.io/ref/7fjaILCsd9AmooIF3MMYz"),
        ("FaucetWorld", "https://faucetworld.in/register?r=157100"),
        ("AltHub", "https://althub.club/r/210922")
    ],
    "Выгодные": [
        ("adBTC", "https://adbtc.top/r/l/4027694"),
        ("BitcoViews", "https://www.bitcoviews.com/ref/Beriya"),
        ("FaucetPayz", "https://faucetpayz.com/ref/Beriya"),
        ("EarnBitMoon", "https://earnbitmoon.club/?ref=1082239"),
        ("BestPayingFaucet", "https://bestpayingfaucet.online/?r=3300"),
        ("EarnTrump", "https://earn-trump.com/?ref=F9IQ")
    ],
    "Все": [
        ("OnlyFaucet", "https://onlyfaucet.com/?r=119284"),
        ("WhoopyRewards", "https://whoopyrewards.com/?r=79573"),
        ("GamerLee", "https://gamerlee.com/?r=9335"),
        ("EarnCryptoWRS", "https://earncryptowrs.in/?r=13740"),
        ("FreeLTC", "https://freeltc.fun/?r=17927"),
        ("Treaw", "https://treaw.com/?r=TUbSeQGBTea2c1uB9tTwhqACPsUYTfs7h6"),
        ("CryptoFuture", "https://cryptofuture.co.in/?r=12285"),
        ("TON Leaks", "https://ton.leaks.work/?ref=6804-3150-9903"),
        ("Help FPCoin", "https://helpfpcoin.site/r/Ti2dBcrS7HL"),
        ("KiddyEarner", "https://kiddyearner.com/?r=Beriya"),
        ("Bagi", "https://bagi.co.in/?ref=100950"),
        ("SatoshiFaucet", "https://satoshifaucet.io/?r=101527"),
        ("CoinAdster", "https://coinadster.com/?ref=317781"),
        ("BanFaucet", "https://banfaucet.com/?r=229451"),
        ("BTC Adspace", "https://btcadspace.com/ref/Beriya"),
        ("LarvelFaucet", "https://larvelfaucet.com/ref/l7KkHQiY"),
        ("FundsReward", "https://fundsreward.com/?r=200553"),
        ("FarazFaucets", "https://farazfaucets.com/?r=67fe8e08cb3c63d6f81e9026"),
        ("ClaimCash", "https://claimcash.cc/?r=22677"),
        ("HateCoin", "https://hatecoin.me/?r=73635"),
        ("SatoshiTap", "https://www.satoshitap.com/ref/Beriya"),
        ("BitcoinGen", "https://bitcoingen.org/?r=10696"),
        ("NatCrypto", "https://natcrypto.com/?r=3249"),
        ("TapCoin", "https://tap-coin.de/refer/user/70058"),
        ("MoonBoom", "https://moonboom.net/?ref=6466"),
        ("Altcryp", "https://altcryp.com/?r=35239"),
        ("Main Site", "https://faucetua.online/")
    ]
}

@bot.message_handler(commands=['start'])
def send_category_selection(message):
    save_user(message.chat.id, message.from_user.username)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Перспективные", callback_data="filter_Перспективные"),
        InlineKeyboardButton("Мультикраны", callback_data="filter_Мультикраны"),
        InlineKeyboardButton("Выгодные", callback_data="filter_Выгодные"),
        InlineKeyboardButton("Все сайты", callback_data="filter_Все"),
        InlineKeyboardButton("Поддержка", callback_data="support")
    )
    bot.send_message(
        message.chat.id,
        "Выберите категорию кранов:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("filter_"))
def send_filtered_links(call):
    cat = call.data.split("_", 1)[1]
    links = categories.get(cat, [])
    markup = InlineKeyboardMarkup(row_width=2)

    # Личный кабинет — первой кнопкой
    markup.add(InlineKeyboardButton("Личный кабинет", url="https://faucetpay.io/?r=8936300"))

    for i in range(0, len(links), 2):
        row = links[i:i+2]
        markup.row(*(InlineKeyboardButton(name, url=url) for name, url in row))

    bot.send_message(call.message.chat.id, f"Категория: {cat}", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "support")
def start_support(call):
    user_states[call.message.chat.id] = "awaiting_support"
    bot.send_message(call.message.chat.id, "Напишите ваше сообщение, и админ получит его.")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) == "awaiting_support")
def handle_support_message(msg):
    user_states[msg.chat.id] = None
    text = f"Сообщение от @{msg.from_user.username or 'Без ника'} (ID: {msg.chat.id}):\n{msg.text}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(msg.chat.id, "Ваше сообщение отправлено администратору.")

if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
