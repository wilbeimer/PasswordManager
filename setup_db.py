import sqlite3

conn = sqlite3.connect("vault.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()
