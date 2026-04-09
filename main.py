# main.py
import os
import sys
import asyncio
import threading
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

# Принудительно сбрасываем буфер вывода
sys.stdout.reconfigure(line_buffering=True)

print("📢 НАЧАЛО ЗАГРУЗКИ main.py", flush=True)

# ========== ЗАГЛУШКА ДЛЯ RAILWAY ==========
app = FastAPI()

@app.get("/")
async def root():
    print("🌐 Запрос к корневому пути", flush=True)
    return {"status": "bot is running"}

# ========== БОТ ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBAPP_URL = "https://tg-game-production-fabe.up.railway.app"

print(f"📢 BOT_TOKEN: {'найден' if BOT_TOKEN else 'НЕ НАЙДЕН!'}", flush=True)
print(f"📢 WEBAPP_URL: {WEBAPP_URL}", flush=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    print(f"✅ ПОЛУЧЕНА КОМАНДА /start от {message.from_user.id}", flush=True)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(
        "🎮 Добро пожаловать в игру!\nНажми на кнопку ниже, чтобы начать.",
        reply_markup=keyboard
    )
    print(f"✅ ОТВЕТ ОТПРАВЛЕН пользователю {message.from_user.id}", flush=True)

async def run_bot():
    print("🤖 БОТ: запускаю polling...", flush=True)
    print(f"🤖 БОТ: WebApp URL = {WEBAPP_URL}", flush=True)
    await dp.start_polling(bot)

def run_bot_in_loop():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    except Exception as e:
        print(f"❌ ОШИБКА БОТА: {e}", flush=True)

# ЗАПУСКАЕМ БОТА СРАЗУ (не в if __name__)
print("📢 ЗАПУСК БОТА В ПОТОКЕ", flush=True)
bot_thread = threading.Thread(target=run_bot_in_loop, daemon=True)
bot_thread.start()
print("📢 ПОТОК БОТА ЗАПУЩЕН", flush=True)

# FastAPI будет запущен через uvicorn командой из Procfile
print("🚀 FastAPI будет запущен отдельно", flush=True)
