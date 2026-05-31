import sqlite3
from datetime import date

def init_db():
    conn = sqlite3.connect("bunaprice.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            code TEXT NOT NULL,
            price_etb REAL NOT NULL,
            volume REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            name TEXT,
            kebele TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            offered_price REAL,
            kebele TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database ready!")

if __name__ == "__main__":
    init_db()