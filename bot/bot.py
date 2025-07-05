import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from db import init_db, add_user, get_points, get_user_count, get_all_users
from messages import START_MESSAGE, HELP_MESSAGE
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN or "")
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id if message.from_user else 0
    username = message.from_user.username if message.from_user and message.from_user.username else "User"
    await add_user(user_id, username)
    points = await get_points(user_id)
    dev = 'Developed by @aenzk\nhttps://t.me/aenzk'
    full_name = message.from_user.full_name if message.from_user and message.from_user.full_name else username
    await message.answer(
        f"{START_MESSAGE}\n\n👤 <b>{full_name}</b>\n💰 <b>Points:</b> <code>{points:.2f}</code>\n\n{dev}",
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_message(message: types.Message):
    await message.answer(HELP_MESSAGE, parse_mode="HTML")

# Admin commands
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "7068007001").split(",") if i.strip().isdigit()]

@dp.message(Command("botstats"))
async def bot_stats(message: types.Message):
    if message.from_user and message.from_user.id in ADMIN_IDS:
        user_count = await get_user_count()
        admin_username = message.from_user.username or "-"
        admin_id = message.from_user.id
        await message.reply(f"<b>Bot Stats</b>\n👤 <b>Admin:</b> @{admin_username} (<code>{admin_id}</code>)\n👥 <b>Total Users:</b> <code>{user_count}</code>", parse_mode="HTML")
    else:
        await message.reply("You are not authorized to use this command.")

@dp.message(Command("userstats"))
async def user_stats(message: types.Message):
    if message.from_user and message.from_user.id in ADMIN_IDS:
        text = "<b>User Stats</b>\n"
        cursor = await get_all_users()
        user_lines = []
        async for user in cursor:
            user_id = user.get('user_id', '-')
            username = user.get('username', '-')
            points = user.get('points', 0.0)
            user_lines.append(f"<b>ID:</b> <code>{user_id}</code> | <b>Username:</b> @{username} | <b>Points:</b> <code>{points:.2f}</code>")
        if user_lines:
            text += "\n".join(user_lines)
        else:
            text += "No users found."
        await message.reply(text, parse_mode="HTML")
    else:
        await message.reply("You are not authorized to use this command.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
