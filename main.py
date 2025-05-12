import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os
from dotenv import load_dotenv
from datetime import datetime
from keep_alive import keep_alive

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
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    user_data = f"{user_id} | @{username or 'NoUsername'} | {date} | 1"

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write(user_data + "\n")
        return

    lines = []
    found = False
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if str(user_id) in line:
                parts = line.strip().split("|")
                parts[-1] = str(int(parts[-1]) + 1)
                lines.append(" | ".join(p.strip() for p in parts) + "\n")
                found = True
            else:
                lines.append(line)

    if not found:
        lines.append(user_data + "\n")

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id, message.from_user.username)
    user_clicks[message.chat.id] = 0

    markup = InlineKeyboardMarkup()
    buttons = [
        ("adBTC", "https://adbtc.top/r/l/4027694"),
        ("ClaimCrypto", "https://claimcrypto.in/?r=1728"),
        ("FireFaucet", "https://firefaucet.win/ref/Beriya1985"),
        ("Assetni", "https://assetni.com/?r=22870"),
        ("OnlyFaucet", "https://onlyfaucet.com/?r=119284"),
        ("WhoopyRewards", "https://whoopyrewards.com/?r=79573"),
        ("WheelOfGold", "https://wheelofgold.com/?r=89784"),
        ("GamerLee", "https://gamerlee.com/?r=9335"),
        ("EarnCryptoWRS", "https://earncryptowrs.in/?r=13740"),
        ("BestPayingFaucet", "https://bestpayingfaucet.online/?r=3300"),
        ("FreeLTC", "https://freeltc.fun/?r=17927"),
        ("EarnSolana", "https://earnsolana.xyz/?r=14425"),
        ("CH3ZO", "https://ch3zo.com/?r=DBBDukPiMV1VsXL1BUPBd5cjtTVJx3uo8P"),
        ("Treaw", "https://treaw.com/?r=TUbSeQGBTea2c1uB9tTwhqACPsUYTfs7h6"),
        ("BitcoViews", "https://www.bitcoviews.com/ref/Beriya"),
        ("CryptoFuture", "https://cryptofuture.co.in/?r=12285"),
        ("TON Leaks", "https://ton.leaks.work/?ref=6804-3150-9903"),
        ("Help FPCoin", "https://helpfpcoin.site/r/Ti2dBcrS7HL"),
        ("KiddyEarner", "https://kiddyearner.com/?r=Beriya"),
        ("EarnTrump", "https://earn-trump.com/?ref=F9IQ"),
        ("Bagi", "https://bagi.co.in/?ref=100950"),
        ("SatoshiFaucet", "https://satoshifaucet.io/?r=101527"),
        ("EFTA Crypto", "https://eftacrypto.com/claim/tron/?r=karamba1199@gmail.com"),
        ("FaucetWorld", "https://faucetworld.in/register?r=157100"),
        ("FaucetPayz", "https://faucetpayz.com/ref/Beriya"),
        ("EarnBitMoon", "https://earnbitmoon.club/?ref=1082239"),
        ("AutoFaucet", "https://autofaucet.dutchycorp.space/?r=Beriya"),
        ("AltHub", "https://althub.club/r/210922"),
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
        ("EarnBonk", "https://earn-bonk.com/?ref=dCwrb"),
        ("NatCrypto", "https://natcrypto.com/?r=3249"),
        ("TapCoin", "https://tap-coin.de/refer/user/70058"),
        ("FaucetCrypto", "https://faucetcrypto.net/?r=86978"),
        ("MoonBoom", "https://moonboom.net/?ref=6466"),
        ("FreePepe", "https://free-pepe.com/?r=110592"),
        ("Altcryp", "https://altcryp.com/?r=35239"),
        ("ClaimFlora", "https://claimflora.com/?r=563"),
        ("SimpleBits", "https://simplebits.io/ref/7fjaILCsd9AmooIF3MMYz"),
        ("Main Site", "https://faucetua.online/")
    ]

    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        markup.row(*(InlineKeyboardButton(text=b[0], url=b[1]) for b in row))

    bot.send_message(
        message.chat.id,
        text=(
            "Добро пожаловать в *FaucetCrypt Bot*!\n\n"
            "Здесь вы найдете лучшие криптовалютные краны и бонусные сайты.\n"
            "Выберите один из вариантов ниже и начните зарабатывать криптовалюту прямо сейчас!"
        ),
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.chat.id
    username = message.from_user.username or "NoUsername"
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if str(user_id) in line:
                    parts = line.strip().split("|")
                    reg_date = parts[2].strip()
                    launches = parts[3].strip()
                    break
            else:
                reg_date = "Неизвестно"
                launches = "0"
    except Exception:
        reg_date = "Ошибка"
        launches = "?"

    bot.send_message(user_id, (
        f"👤 *Ваш профиль*\n\n"
        f"ID: `{user_id}`\n"
        f"Username: @{username}\n"
        f"Дата регистрации: {reg_date}\n"
        f"Запусков бота: {launches}"
    ), parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
