import pandas as pd
import sqlite3
import json


def read_csv(filepath):
    df = pd.read_csv(filepath,sep=';')
    return df


def save_json(df,filename):
    df.to_json(f'./Answers/{filename}.json', orient='records', lines=True)


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file) 
    return pd.DataFrame(data)


def push_to_sql(df,tableName):
    try:
        conn = sqlite3.connect('database.db')
        df.to_sql(tableName, conn, if_exists='replace', index=False)
        return True
    except:
        return False


def connect_db(db_name):
    return sqlite3.connect(db_name)


def first_ten_row(db_name, n, sort_field):
    conn = connect_db(db_name)
    query = f'''
    SELECT * FROM task3
    ORDER BY {sort_field}
    LIMIT {n}
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def statistics(db_name, numeric_field):
    conn = connect_db(db_name)
    query = f'''
    SELECT 
        SUM({numeric_field}) AS total,
        MIN({numeric_field}) AS minimum,
        MAX({numeric_field}) AS maximum,
        AVG({numeric_field}) AS average
    FROM task3
    '''
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def frequency(db_name, categorical_field):
    conn = connect_db(db_name)
    query = f'''
    SELECT {categorical_field}, COUNT(*) AS frequency
    FROM task3
    GROUP BY {categorical_field}
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def filtered_rows(db_name, n, predicate, sort_field):
    conn = connect_db(db_name)
    query = f'''
    SELECT * FROM task3
    WHERE {predicate}
    ORDER BY {sort_field}
    LIMIT {n}
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


filepath = './55/3/_part_1.csv'
filepath2 = './55/3/_part_2.json'
df1 = read_csv(filepath)
df2 = read_json_file(filepath2)


result_df = pd.concat([df1,df2],axis=1,keys=['atrtist','song'])
result_df.columns = ['_'.join(col).strip() for col in result_df.columns.values]


push_to_sql(result_df,'task3')


def third_task():
    db_name = 'database.db' 
    
    df = first_ten_row(db_name, 10, 'atrtist_duration_ms')
    save_json(df,'task3_1')

    stats = statistics(db_name, 'atrtist_tempo')
    print(stats)

    df = frequency_df = frequency(db_name, 'atrtist_genre')
    save_json(df,'task3_2')

    df = filtered_rows(db_name, 15, "atrtist_energy > 0.5", 'atrtist_energy')
    save_json(df,'task3_3')



if __name__ == '__main__':
    third_task()