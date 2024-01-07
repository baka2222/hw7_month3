from pathlib import Path
import sqlite3


def init_db():
    global db, cursor
    db_path = Path(__file__).parent.parent / 'HouseKg.db'
    db = sqlite3.connect(db_path)
    cursor = db.cursor()


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS houses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    header TEXT,
    price TEXT,
    address TEXT,
    description TEXT)''')
    db.commit()


def fill_table(title, prc, adrs, descript):
    cursor.execute(f'''INSERT INTO houses (header, price, address, description)
    VALUES ("{title}", "{prc}", "{adrs}", "{descript}")''')
    db.commit()

init_db()
create_table()
