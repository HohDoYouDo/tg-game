# main.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBAPP_URL = "https://tg-game-production-fabe.up.railway.app"  # твой URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(
        "🎮 Добро пожаловать в игру!\nНажми на кнопку ниже, чтобы начать.",
        reply_markup=keyboard
    )
    print(f"✅ /start от {message.from_user.id}")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Отправь /start, чтобы начать игру!")

async def main():
    print("🤖 Бот запущен и готов к работе!")
    print(f"🌐 WebApp URL: {WEBAPP_URL}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🚀 Запускаем бота...")
    asyncio.run(main())
