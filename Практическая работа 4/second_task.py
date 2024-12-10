import pandas as pd
import sqlite3
import json


def json_to_df(filepath):
    try:
        df = pd.read_json(filepath,encoding='utf-8')
        return df
    except FileNotFoundError:
        return None


def push_to_sql(df):
    try:
        conn = sqlite3.connect('database.db')
        df.to_sql('task2', conn, if_exists='replace', index=False)
        return True
    except:
        return False


def save_json(data):
    with open('./Answers/second_task.json', 'w',encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4,ensure_ascii=False)


def pickle_to_df(filepath):
    try:
        df = pd.read_pickle(filepath)
        return df
    except FileNotFoundError:
        return None


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file) 
    return data


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query1 = """CREATE TABLE IF NOT EXISTS task2_1 (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    street TEXT,
    city TEXT,
    zipcode INTEGER,
    floors INTEGER,
    year INTEGER,
    parking INTEGER,
    prob_price REAL,
    views INTEGER
    );"""

    query2 = """
    CREATE TABLE IF NOT EXISTS task2_2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT,
    rating REAL,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT,
    FOREIGN KEY (building_name) REFERENCES task2_1(name)
    );"""

    cursor.execute(query1)
    cursor.execute(query2)
    conn.commit()
    conn.close()


def insert_data(origin_data, description_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO task2_1 (id, name, street, city, zipcode, floors, year, parking, prob_price, views) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (origin_data['id'], origin_data['name'], origin_data['street'],
              origin_data['city'], origin_data['zipcode'], origin_data['floors'],
              origin_data['year'], origin_data['parking'], origin_data['prob_price'],
              origin_data['views']))

        cursor.execute('''
            INSERT INTO task2_2 (building_name, rating, convenience, security, functionality, comment) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (description_data['name'], description_data['rating'], description_data['convenience'],
              description_data['security'], description_data['functionality'], description_data['comment']))

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  

    finally:
        cursor.close()
        conn.close()



def insert_json(json1,json2):
    for i,value in enumerate(json1):
        origin_data = value
        description_data = json2[i]
        insert_data(origin_data, description_data)


def query1():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query1 = '''
    SELECT t1.name, t1.city, t1.street, t2.rating, t2.convenience, t2.security, t2.functionality, t2.comment
    FROM task2_1 t1
    LEFT JOIN task2_2 t2 ON t1.name = t2.building_name
    '''
    cursor.execute(query1)
    results1 = cursor.fetchall()
    print("Все здания с их описанием")
    for row in results1:
        print(row)
    cursor.close()
    conn.close()


def query2():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query2 = '''
    SELECT rating, COUNT(*) as building_count
    FROM task2_2
    GROUP BY rating
    '''
    cursor.execute(query2)
    results2 = cursor.fetchall()
    print("Подсчет количество зданий по рейтингу")
    for row in results2:
        print(f"Rating: {row[0]}, Count: {row[1]}")
    cursor.close()
    conn.close()


def query3():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query3 = '''
    SELECT t1.name, t1.city, t1.street
    FROM task2_1 t1
    JOIN task2_2 t2 ON t1.name = t2.building_name
    WHERE t2.convenience = ?
    '''
    cursor.execute(query3, (5,))
    results3 = cursor.fetchall()
    print(f"Здания с уровнем {5}")
    for row in results3:
        print(row)
    cursor.close()
    conn.close()


def second_task():
    filepath = './55/1-2/subitem.json'
    df = json_to_df(filepath)
    push_to_sql(df)

    create_tables()

    origin_json = pickle_to_df('./55/1-2/item.pkl')
    description_json = read_json_file(filepath)
    insert_json(origin_json,description_json)
    print(query1())
    print(query2())
    print(query3())


if __name__ == '__main__':
    second_task()