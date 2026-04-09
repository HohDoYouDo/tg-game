# main.py
import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

# ========== ЗАГЛУШКА ДЛЯ RAILWAY (чтобы не ругался) ==========
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "bot is running (no web game)"}

# ========== БОТ ==========
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

async def run_bot():
    print("🤖 Бот запущен и готов!")
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
    
    # Запускаем FastAPI (заглушку) в главном потоке
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 FastAPI-заглушка на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
