import os
import sqlite3
from config import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS sellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL UNIQUE,
        score INTEGER NOT NULL DEFAULT 0
    )''')

    connection.commit()
    connection.close()

def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('PRAGMA journal_mode=WAL;')
    connection.execute('PRAGMA busy_timeout=5000;')
    connection.row_factory = sqlite3.Row
    return connection