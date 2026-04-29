import aiosqlite
import os

DB_PATH = "stock_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def log_interaction(user_id: str, message: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO logs (user_id, message) VALUES (?, ?)", (user_id, message))
        await db.commit()

async def add_to_watchlist(user_id: str, symbol: str):
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if already exists
        async with db.execute("SELECT id FROM watchlist WHERE user_id = ? AND symbol = ?", (user_id, symbol)) as cursor:
            if await cursor.fetchone():
                return False
        await db.execute("INSERT INTO watchlist (user_id, symbol) VALUES (?, ?)", (user_id, symbol))
        await db.commit()
        return True

async def remove_from_watchlist(user_id: str, symbol: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM watchlist WHERE user_id = ? AND symbol = ?", (user_id, symbol))
        await db.commit()
        return True

async def get_watchlist(user_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT symbol FROM watchlist WHERE user_id = ?", (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
