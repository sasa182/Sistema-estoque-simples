import sqlite3


DB_PATH = 'db/stock.db'
HISTORY_DB_PATH = 'db/history.db'

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def create_registry_table():
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            operation TEXT,
            date TEXT,
            quantity INTEGER,
            old_price REAL,
            price REAL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    conn.commit()
    conn.close()


def clear_table_reset_id(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # limpa tabela
    cursor.execute(f'DELETE FROM {table_name}')
    # reseta id
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # criação inicial das tabelas
    create_db()
    create_registry_table()

    reset_db = input('> RESET DATABASE? (y) ')
    if reset_db == 'y':
        clear_table_reset_id(DB_PATH, 'products')
        clear_table_reset_id(HISTORY_DB_PATH, 'products_history')
    