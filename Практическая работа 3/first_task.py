import os

import os
import json
import pandas as pd
from bs4 import BeautifulSoup


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
    

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# загрузка информации из файла в словарь
def get_html_data(filepath):
    soup = upload_file(filepath)

    city = soup.find('span').text.strip().split(': ')[1]
    title = soup.find('h1', class_='title').text.strip().split(':')[1]
    address = soup.find('p', class_='address-p').text.strip().replace('Улица:', '').replace('Индекс:', '').strip()
    floors = int(soup.find('span', class_='floors').text.strip().split(': ')[1])
    year_built = int(soup.find('span', class_='year').text.strip().split(' ')[-1])
    parking = soup.find_all('span')[3].text.strip().split(':')[1]
    rating = float(soup.find_all('span')[4].text.strip().split(':')[1])
    views = int(soup.find_all('span')[5].text.strip().split(': ')[1])
    
    result = {
        'city': city,
        'title': title,
        'address': address,
        'floors': floors,
        'year_built': year_built,
        'parking': parking,
        'rating': rating,
        'views': views
    }

    return result


# функция получения данных из всех файлов
def read_files(folderpath):
    data_list = list()

    for filename in os.listdir(folderpath):
        if filename.endswith('.html'):
            file_path = os.path.join(folderpath, filename)
            data = get_html_data(file_path)
            data_list.append(data)

    return data_list


def sort_data(df):
    return df.sort_values(by='rating')


def filtre_data(df):
    return df[df['parking'] == 'нет']


def calculate_statistic(df):
    _sum = df['views'].sum()
    _min = df['views'].min()
    _max = df['views'].max()
    _avg = df['views'].mean()

    return _sum, _min, _max, _avg


def calculate_frequency(df):
    return df['city'].value_counts()


def print_result(title, data):
      if type(data) == list:
            print('\n','='*15,'\n',
                  title,'\n\n',
                  *data,'\n',
                  '='*15,'\n')
      else:
            print('\n','='*15,'\n',
                  title,'\n\n',
                  data,'\n',
                  '='*15,'\n')
            

def first_task(folderpath):
    # получим список словарей с данными из html
        data = read_files(folderpath)

        df = create_dataframe(data)
        # отсортируйте значения по одному из доступных полей
        sorted_df = sort_data(df)
        print_result('Sorted df:', sorted_df)

        # выполните фильтрацию по другому полю (запишите результат отдельно)
        filtre_df = filtre_data(df)
        print_result('Filtred df:', filtre_df)
        # для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
        summ, minn, maxx, avgg = calculate_statistic(df)
        print_result('Params:\n',[
                     f'sum: {summ}',
                     f'min: {minn}',
                     f'max: {maxx}',
                     f'avg: {avgg}'])

        # для одного текстового поля посчитайте частоту меток
        frequency = calculate_frequency(df)
        print_result('Frequency:', frequency)

        save_json(data,'./Answers/first_task/first_task.json')
        print('Saving data to json True')


if __name__ == '__main__':
    first_task('./55/1')