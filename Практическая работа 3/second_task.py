import os
import json

import pandas as pd
from bs4 import BeautifulSoup


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# Загрузка файла
def upload_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup


def create_dataframe(data):
    try:
        return pd.DataFrame(data)
    except:
        print('Error while creating dataframe')
        return None
    

# загрузка информации из файла в словарь
def get_html_data(filepath):
    soup = upload_file(filepath)
    products = []

    for product_item in soup.find_all('div', class_='product-item'):
        product = {}
        product_name = product_item.find('span').text.strip()
        product['name'] = product_name
        
        price_text = product_item.find('price').text.strip().replace('₽', '').replace(' ', '')
        product['price'] = int(price_text) if price_text.isdigit() else None
        
        product['ram'] = None
        product['camera'] = None
        product['acc'] = None
        product['processor'] = None
        product['sim'] = None
        product['matrix'] = None
        product['resolution'] = None
        
        for el in product_item.find_all('li'):
            char_type = el.get('type')
            char_value = el.text.strip()
            if char_type in product:
                product[char_type] = char_value
            
        products.append(product)

    return products


# функция получения данных из всех файлов
def read_files(folderpath):
    data_list = list()

    for filename in os.listdir(folderpath):
        if filename.endswith('.html'):
            file_path = os.path.join(folderpath, filename)
            data = get_html_data(file_path)
            data_list.extend(data)

    return data_list


def second_task(folderpath):
    data = read_files(folderpath)
    df = create_dataframe(data)

    sorted_df = df.sort_values(by='price', ascending=True)
    print(sorted_df)

    filtered_df = df[df['sim'] == '3 SIM']
    print(filtered_df)

    price_sum = df['price'].sum()
    price_min = df['price'].min()
    price_max = df['price'].max()
    price_avg = df['price'].mean()

    print(f"Sum: {price_sum}, Min: {price_min}, Max: {price_max}, Average: {price_avg}")

    processor_frequency = df['processor'].value_counts()
    print(processor_frequency)

    save_json(data, './Answers/second_task/second_task.json')


if __name__ == '__main__':
    second_task('./55/2')