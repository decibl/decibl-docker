import sqlite3

# database library

# make database "data"


def make_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, item_id INTEGER, q TEXT)')
    conn.commit()
    conn.close()

# add data to database


def add_data(item_id, q):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO data (item_id, q) VALUES (?, ?)', (item_id, q))
    conn.commit()
    conn.close()

# get data from database


def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    data = c.fetchall()
    conn.close()
    return data
