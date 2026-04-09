# main.py
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import sqlite3
import os
import asyncio
import threading
from contextlib import asynccontextmanager

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

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
