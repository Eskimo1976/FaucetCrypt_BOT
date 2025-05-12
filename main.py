import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Приветственное сообщение
WELCOME_MESSAGE = """
<b>Добро пожаловать в FaucetBot!</b>

Здесь вы найдете лучшие крипто-краны и сайты для заработка криптовалюты!

Выберите любой из предложенных вариантов ниже:

Также можете посетить наш сайт:
"""

# Основная ссылка на сайт
MAIN_SITE_URL = "https://faucetua.online/"

# Список кранов
FAUCET_LINKS = [
    "https://adbtc.top/r/l/4027694",
    "https://claimcrypto.in/?r=1728",
    "https://firefaucet.win/ref/Beriya1985",
    "https://assetni.com/?r=22870",
    "https://onlyfaucet.com/?r=119284",
    "https://whoopyrewards.com/?r=79573",
    "https://wheelofgold.com/?r=89784",
    "https://gamerlee.com/?r=9335",
    "https://earncryptowrs.in/?r=13740",
    "https://bestpayingfaucet.online/?r=3300",
    "https://freeltc.fun/?r=17927",
    "https://earnsolana.xyz/?r=14425",
    "https://ch3zo.com/?r=DBBDukPiMV1VsXL1BUPBd5cjtTVJx3uo8P",
    "https://treaw.com/?r=TUbSeQGBTea2c1uB9tTwhqACPsUYTfs7h6",
    "https://www.bitcoviews.com/ref/Beriya",
    "https://cryptofuture.co.in/?r=12285",
    "https://ton.leaks.work/?ref=6804-3150-9903",
    "https://helpfpcoin.site/r/Ti2dBcrS7HL",
    "https://kiddyearner.com/?r=Beriya",
    "https://earn-trump.com/?ref=F9IQ",
    "https://bagi.co.in/?ref=100950",
    "https://satoshifaucet.io/?r=101527",
    "https://eftacrypto.com/claim/tron/?r=karamba1199@gmail.com",
    "https://faucetworld.in/register?r=157100",
    "https://faucetpayz.com/ref/Beriya",
    "https://earnbitmoon.club/?ref=1082239",
    "https://autofaucet.dutchycorp.space/?r=Beriya",
    "https://althub.club/r/210922",
    "https://coinadster.com/?ref=317781",
    "https://banfaucet.com/?r=229451",
    "https://btcadspace.com/ref/Beriya",
    "https://larvelfaucet.com/ref/l7KkHQiY",
    "https://fundsreward.com/?r=200553",
    "https://farazfaucets.com/?r=67fe8e08cb3c63d6f81e9026",
    "https://claimcash.cc/?r=22677",
    "https://hatecoin.me/?r=73635",
    "https://www.satoshitap.com/ref/Beriya",
    "https://bitcoingen.org/?r=10696",
    "https://earn-bonk.com/?ref=dCwrb",
    "https://natcrypto.com/?r=3249",
    "https://tap-coin.de/refer/user/70058",
    "https://faucetcrypto.net/?r=86978",
    "https://kiddyearner.com/?r=Beriya",
    "https://moonboom.net/?ref=6466",
    "https://free-pepe.com/?r=110592",
    "https://altcryp.com/?r=35239",
    "https://assetni.com/?r=22870",
    "https://claimflora.com/?r=563",
    "https://simplebits.io/ref/7fjaILCsd9AmooIF3MMYz",
]

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Формируем клавиатуру с кнопками по две в ряд
    keyboard = InlineKeyboardMarkup(row_width=2)

    for link in FAUCET_LINKS:
        btn = InlineKeyboardButton(text="Открыть кран", url=link)
        keyboard.add(btn)

    # Добавляем ссылку на основной сайт
    keyboard.add(InlineKeyboardButton(text="Наш сайт", url=MAIN_SITE_URL))

    await message.answer(WELCOME_MESSAGE, reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
