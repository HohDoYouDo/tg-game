# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

print("📢 ЗАПУСК БОТА")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBAPP_URL = "https://tg-game-production-fabe.up.railway.app"  # твой URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    print(f"✅ /start от {message.from_user.id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(
        "🎮 Нажми на кнопку ниже, чтобы открыть игру.",
        reply_markup=keyboard
    )

async def main():
    print("🤖 Бот запущен и готов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
