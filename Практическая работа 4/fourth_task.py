import pandas as pd
import sqlite3
import json


def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK(price >= 0),
        quantity INTEGER NOT NULL CHECK(quantity >= 0),
        category TEXT,
        fromCity TEXT,
        isAvailable BOOLEAN,
        views INTEGER,
        update_counter INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()




def load_products_from_json(db_name, json_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    for product in products:
        cursor.execute('''
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            price = excluded.price,
            quantity = excluded.quantity,
            category = excluded.category,
            fromCity = excluded.fromCity,
            isAvailable = excluded.isAvailable,
            views = excluded.views,
            update_counter = update_counter + 1
        ''', (product['name'], product['price'], product['quantity'], product.get('category'), 
              product['fromCity'], product['isAvailable'], product['views']))
    
    conn.commit()
    conn.close()


def process_commands_from_csv(db_name, csv_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    df = pd.read_csv(csv_file, sep=';')
    
    for _, row in df.iterrows():
        name = row['name']
        method = row['method']
        param = row['param']
        
        if method == 'available':
            cursor.execute('''
            UPDATE products
            SET isAvailable = ?, update_counter = update_counter + 1
            WHERE name = ?
            ''', (param == 'True', name))
        
        elif method == 'remove':
            cursor.execute('DELETE FROM products WHERE name = ?', (name,))
        
        elif method == 'quantity_add':
            cursor.execute('''
            UPDATE products
            SET quantity = quantity + ?, update_counter = update_counter + 1
            WHERE name = ?
            ''', (int(param), name))
        
        elif method == 'price_abs':
            cursor.execute('''
            UPDATE products
            SET price = ?, update_counter = update_counter + 1
            WHERE name = ? AND ? >= 0
            ''', (float(param), name, float(param)))
        
        elif method == 'price_percent':
            cursor.execute('''
            UPDATE products
            SET price = price * (1 + ?), update_counter = update_counter + 1
            WHERE name = ?
            ''', (float(param), name))
    
    conn.commit()
    conn.close()


def display_top_updated_products(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT name, update_counter
    FROM products
    ORDER BY update_counter DESC
    LIMIT 10
    ''')
    
    results = cursor.fetchall()
    conn.close()
    return results



def analyze_prices(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT AVG(price), MIN(price), MAX(price)
    FROM products
    WHERE isAvailable = 1
    ''')
    
    results = cursor.fetchone()
    conn.close()
    return results


def fourth_task():
    create_database('database.db')
    load_products_from_json('database.db', './55/4/_product_data.json')
    process_commands_from_csv('database.db', './55/4/_update_data.csv')

    top_updated = display_top_updated_products('database.db')
    print('Топ 10 товаров')
    for product in top_updated:
        print(product)
    print('\n')
    price_analysis = analyze_prices('database.db')
    print("Среднее, Максимальное, минимальное:", price_analysis)


if __name__ == '__main__':
    fourth_task()


