import sqlite3

import config

# database library

# make database "data"
def make_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    conn.commit()
    conn.close()

# add data to database
def add_data(item_id, q):
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    
    conn.commit()
    conn.close()

# get data from database
def get_data():
    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    data = c.fetchall()
    conn.close()

    return data
