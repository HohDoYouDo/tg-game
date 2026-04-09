# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import os
import asyncio
import threading
import time

# ========== БАЗА ДАННЫХ ==========
def init_db():
    conn = sqlite3.connect('game.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def update_score(user_id: int, username: str, score: int):
    conn = sqlite3.connect('game.db')
    cur = conn.execute('SELECT score FROM players WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    if row:
        if score > row[0]:
            conn.execute('UPDATE players SET score = ? WHERE user_id = ?', (score, user_id))
    else:
        conn.execute('INSERT INTO players (user_id, username, score) VALUES (?, ?, ?)',
                     (user_id, username, score))
    conn.commit()
    conn.close()

def get_top():
    conn = sqlite3.connect('game.db')
    rows = conn.execute('SELECT username, score FROM players ORDER BY score DESC LIMIT 10').fetchall()
    conn.close()
    return [{'username': r[0], 'score': r[1]} for r in rows]

init_db()

# ========== FASTAPI ==========
app = FastAPI()

@app.get('/')
async def game_page():
    with open('game.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(f.read())

@app.get('/api/score')
async def save_score(user_id: int, username: str, score: int):
    update_score(user_id, username, score)
    return {'ok': True}

@app.get('/api/top')
async def get_top_scores():
    return get_top()

# ========== БОТ ДЛЯ aiogram 3.x ==========
def run_bot():
    import asyncio
    from aiogram import Bot, Dispatcher, types
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    from aiogram.filters import Command
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не найден! Добавь переменную окружения BOT_TOKEN")
        return
    
    # ТВОЙ РЕАЛЬНЫЙ URL (тот, который работает в браузере)
    WEBAPP_URL = "https://tg-game-production-fabe.up.railway.app"
    
    print(f"🤖 Бот запускается. WebApp URL: {WEBAPP_URL}")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def start_cmd(message: types.Message):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await message.answer("🎮 Нажимай на красный круг! У тебя 30 секунд.", reply_markup=keyboard)
        print(f"✅ /start от {message.from_user.id}")
    
    async def main():
        print("✅ Бот готов, запускаем polling...")
        await dp.start_polling(bot)
    
    asyncio.run(main())

def start_bot_delayed():
    time.sleep(3)
    print("🚀 Запускаем бота...")
    run_bot()

# Запускаем бота в отдельном потоке
threading.Thread(target=start_bot_delayed, daemon=True).start()

# ========== ЗАПУСК FASTAPI ==========
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 FastAPI запускается на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
