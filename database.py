import sqlite3

database = sqlite3.connect('users.db')
cur = database.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS history(
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id BIGINT,
    full_name TEXT, 
    first_lang TEXT,
    second_lang TEXT,
    original_text TEXT,
    translated_text TEXT
    )
    """)

database.commit()
database.close()
