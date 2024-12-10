import pandas as pd
import sqlite3
import json


def pickle_to_df(filepath):
    try:
        df = pd.read_pickle(filepath)
        df = pd.DataFrame(df)
        return df
    except FileNotFoundError:
        return None


def push_to_sql(df):
    try:
        conn = sqlite3.connect('database.db')
        df.to_sql('task1', conn, if_exists='replace', index=False)
        return True
    except:
        return False


def save_json(data,filename):
    with open(f'./Answers/{filename}.json', 'w',encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4,ensure_ascii=False)


def get_first_rows(tableName):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM {tableName} ORDER BY city LIMIT 10;"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()
    return rows, column_names


def count_statistic(tableName):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT 
                SUM(year) AS total_sum,
                MIN(year) AS min_value,
                MAX(year) AS max_value,
                AVG(year) AS average_value
            FROM {tableName};"""
    cursor.execute(query)
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    total_sum, min_value, max_value, average_value = result
    return total_sum, min_value, max_value, average_value 


def count_frequency(tableName):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT 
                city, 
                COUNT(*) AS frequency
            FROM {tableName}
            GROUP BY city;
            """
    cursor.execute(query)
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


def get_filtred_data(tableName):
    filter_predicate = 'year > 1750'
    numeric_field = 'year'
    num_rows = 10

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = f"""SELECT * 
                FROM {tableName} 
                WHERE {filter_predicate} 
                ORDER BY {numeric_field} 
                LIMIT {num_rows};"""
    
    cursor.execute(query)
    results = cursor.fetchall() 
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    return results, column_names


def first_task():

    filepath = './55/1-2/item.pkl'
    df = pickle_to_df(filepath)
    push_to_sql(df)

    rows, column_names = get_first_rows('task1')
    results = [dict(zip(column_names, row)) for row in rows]
    save_json(results,'first_name_1')

    total_sum, min_value, max_value, average_value = count_statistic('task1')
    print(f"Сумма: {total_sum}")
    print(f"Минимум: {min_value}")
    print(f"Максимум: {max_value}")
    print(f"Среднее: {average_value}")

    result = count_frequency('task1')
    print('Часота встречаемости для поля city')
    print(result)

    data, column_names = get_filtred_data('task1')
    results = [dict(zip(column_names, row)) for row in data]
    save_json(results,'first_task_2')


if __name__ == '__main__':
    first_task()