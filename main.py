# main.py
import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

# ========== ЗАГЛУШКА ДЛЯ RAILWAY (чтобы не искал app) ==========
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "bot is running"}

# ========== БОТ ==========
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

async def run_bot():
    print("🤖 Бот запущен и готов к работе!")
    print(f"🌐 WebApp URL: {WEBAPP_URL}")
    await dp.start_polling(bot)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    import threading
    import uvicorn
    
    # Запускаем бота в отдельном потоке
    def start_bot():
        asyncio.run(run_bot())
    
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем FastAPI в главном потоке (чтобы Railway не ругался)
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 FastAPI (заглушка) запускается на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
