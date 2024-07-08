import asyncio
import logging
from datetime import datetime
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import psycopg2

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("py_log.log", mode='w'),
                        logging.StreamHandler()
                    ])

parms_for_postgesql = {
    "dbname": "users_bd",
    "user": "salamat",
    "password": "QWE123",
    "host": "localhost",
    "port": 5432
}

conn = psycopg2.connect(**parms_for_postgesql)
cursor = conn.cursor()

def save_message_to_db(message_text):
    cursor.execute("INSERT INTO messages (message_text) VALUES (%s)", (message_text,))
    conn.commit()

TELEGRAM_BOT_KEY = "7488365215:AAEXO-Aswml3_MN5IoX_5uGChDORyDAzkko"
bot = Bot(token=TELEGRAM_BOT_KEY)
dp = Dispatcher()

@dp.message(F.text == '/start')
async def start(message:Message):
    await message.answer("/timer /rps")

@dp.message(F.text == '/timer')
async def timer_command(message: Message):
    start_time = datetime.now()
    await message.answer(f"Таймер запущен в {start_time.strftime('%H:%M:%S')}")
    await asyncio.sleep(5)
    end_time = datetime.now()
    await message.answer(f"Таймер завершен в {end_time.strftime('%H:%M:%S')}")

@dp.message(F.text == '/rps')
async def rps_command(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Камень')],
            [KeyboardButton(text='Ножницы')],
            [KeyboardButton(text='Бумага')]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите: Камень, Ножницы или Бумага", reply_markup=markup)

@dp.message(F.text.in_({"Камень", "Ножницы", "Бумага"}))
async def rps_game(message: Message):
    choices = ["Камень", "Ножницы", "Бумага"]
    bot_choice = random.choice(choices)
    user_choice = message.text

    if user_choice == bot_choice:
        result = "Ничья!"
    elif (user_choice == "Камень" and bot_choice == "Ножницы") or \
         (user_choice == "Ножницы" and bot_choice == "Бумага") or \
         (user_choice == "Бумага" and bot_choice == "Камень"):
        result = "Вы выиграли!"
    else:
        result = "Бот выиграл!"

    await message.answer(f"Вы выбрали: {user_choice}\nБот выбрал: {bot_choice}\n{result}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
