import sqlite3
import tkinter as tk
from datetime import datetime
import csv


DB_PATH = 'db/stock.db'
HISTORY_DB_PATH = 'db/history.db'
BALANCE_PATH = 'sales balance/balance.csv'

''' -----------------------------------------------------------------------------------------------------
'''

#? MAIN FUNCTIONS
# adiciona produto na db
def add_product(name, quantity, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO products (name, quantity, price)
    VALUES(?, ?, ?)
    ''', (name, quantity, price))

    product_id = cursor.lastrowid # obtem id do prod

    conn.commit()
    conn.close()

    # log operation
    log_operation(product_id, 'addition', quantity, old_price=None, price=price)

    print(f"Produto '{name}' adicionado com sucesso!")


# mostra a db
def list_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products


# filtra / pesquisa a db pelo nome ou id
def search_product(search_term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM products WHERE name = ? OR id=?
    ''', (search_term, search_term))
    results = cursor.fetchall()
    conn.close()
    return results


# apaga um produto da db
def remove_product(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()

    # log operation
    log_operation(product_id, 'removal', None, old_price=None, price=None)

    print(f"Produto com id '{product_id}' foi removido com sucesso!")


# da baixa do produto -venda (abaixa sua quantidade)
def record_product(product_id, sale_quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT quantity, price from products WHERE id = ?
    ''', (product_id,))
    result = cursor.fetchone()

    if result:
        current_quantity, current_price = result
        if current_quantity >= sale_quantity:
            cursor.execute('''
            UPDATE products
            SET quantity = quantity - ?
            WHERE id = ?
            ''', (sale_quantity, product_id))
            conn.commit()
            # * usar placeholders: ? (variable) é melhor q f strings pq previne contra sql injection

            # log operation
            log_operation(product_id, 'sale', -(sale_quantity), old_price=None, price=current_price)
            # add to balance
            add_to_balance(value=current_price * sale_quantity)

            print(f"Produto de id '{product_id}' teve baixa com sucesso!")
        else:
            print(f"Não é possível dar baixa no produto de id '{product_id}' pois a quantidade desejada é maior que a disponível!")
    conn.close()


# ajuta o preço do produto
def update_price(product_id, new_price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT quantity, price FROM products WHERE id = ?
    ''', (product_id,))
    result= cursor.fetchone()

    if result:
        quantity, old_price = result
        cursor.execute('''
        UPDATE products
        SET price = ?
        WHERE id = ?
        ''', (new_price, product_id))
        conn.commit()

        # log operation
        log_operation(product_id, 'price_change', quantity, old_price, new_price)

        print(f"Produto de id '{product_id}' teve o preço alterado com sucesso! [R($) {new_price}]")
    else:
        print(f"Produto de id '{product_id}' não encontrado.")
    conn.close()


''' -----------------------------------------------------------------------------------------------------
'''

# ? VISÃO EM TEMPO  REAL
# Função para buscar dados do banco
def fetch_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Função para atualizar a Treeview em tempo real
def update_view(tree, db_path, table_name):
    for row in tree.get_children():
        tree.delete(row)
    rows = fetch_data(db_path, table_name)
    if table_name == 'products_history':
        for row in rows:
            tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4], row[5], row[6]))
    else:
        for row in rows:
            tree.insert("", tk.END, values=row)
    tree.after(1000, lambda: update_view(tree, db_path, table_name))


''' -----------------------------------------------------------------------------------------------------
'''

#? LOGS
def log_operation(product_id, operation, quantity, old_price=None, price=None):
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO products_history (product_id, operation, date, quantity, old_price, price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_id, operation, date, quantity, old_price, price))

    conn.commit()
    conn.close()


''' -----------------------------------------------------------------------------------------------------
'''

#? BALANCE
def add_to_balance(value):
    with open(BALANCE_PATH, newline='') as csvfile:
        old_balance = float(list(csv.reader(csvfile))[-1][-1])
        with open(BALANCE_PATH, 'a', newline='') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_balance = f'{(old_balance + value):.2f}'
            writer = csv.writer(f)
            writer.writerow([date, value, new_balance])

