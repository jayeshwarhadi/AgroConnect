import sqlite3
from config import Config

def connect_db():
    return sqlite3.connect(Config.DATABASE, check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT "seller"
        )
    ''')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            subscription_active INTEGER DEFAULT 0,
            trial_end_date TEXT DEFAULT NULL
        )
    """)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (seller_id) REFERENCES sellers(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

# Call this function once to create tables
create_tables()