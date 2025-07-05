import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db import init_db, add_user, get_points, get_user_count, get_all_users
from messages import START_MESSAGE, HELP_MESSAGE
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://t.me/monetag_earning_pro_bot/earn')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN or "")
dp = Dispatcher()




@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id if message.from_user else 0
    username = message.from_user.username if message.from_user and message.from_user.username else "User"
    await add_user(user_id, username)
    points = await get_points(user_id)
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='Open Earning App', web_app=WebAppInfo(url=WEBAPP_URL)))
    dev = 'Developed by @aenzk\nhttps://t.me/aenzk'
    full_name = message.from_user.full_name if message.from_user and message.from_user.full_name else username
    await message.answer(
        f"{START_MESSAGE}\n\n� {full_name}\n💰 Points: {points:.2f}\n\n{dev}",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

@dp.message(Command("help"))
async def help_message(message: types.Message):
    await message.answer(HELP_MESSAGE, parse_mode="Markdown")

@dp.message(Command("points"))
async def show_points(message: types.Message):
    user_id = message.from_user.id if message.from_user else 0
    points = await get_points(user_id)
    await message.reply(f"You have {points:.2f} points.")


# Admin commands
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "7068007001").split(",") if i.strip().isdigit()]

@dp.message(Command("botstats"))
async def bot_stats(message: types.Message):
    if message.from_user and message.from_user.id in ADMIN_IDS:
        user_count = await get_user_count()
        await message.reply(f"Bot Stats:\nTotal Users: {user_count}\nAdmin: @aenzk (7068007001)")
    else:
        await message.reply("You are not authorized to use this command.")

@dp.message(Command("userstats"))
async def user_stats(message: types.Message):
    if message.from_user and message.from_user.id in ADMIN_IDS:
        text = "User Stats:\n"
        cursor = await get_all_users()
        async for user in cursor:
            text += f"ID: {user['user_id']} | Username: {user.get('username', '-')}, Points: {user.get('points', 0.0)}\n"
        await message.reply(text or "No users found.")
    else:
        await message.reply("You are not authorized to use this command.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
