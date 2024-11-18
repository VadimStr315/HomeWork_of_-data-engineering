import os
import re
import csv
import math 

import requests
import pandas as pd


# сохранение в файл
def save_file(path, dict_):
    with open(path, 'w', encoding='utf-8') as file:
        for k, v in dict_.items():
            file.write(f"{k}:{v}\n")
    print('Saving True')


# получение датафрейма
def get_dataframe(path):
    dataframe = pd.read_csv(path)
    return dataframe


def make_task(dataframe):
    # 1. Удалите из таблицы столбец description
    dataframe.drop('description',axis = 1, inplace = True)
    # 2. Найдите среднее арифметическое по столбцу quantity
    mean = float(dataframe['quantity'].mean())
    # 3. Найдите максимум по столбцу quantity
    max_value = int(dataframe['quantity'].max())
    # 4. Найдите минимум по столбцу quantity
    min_value = int(dataframe['quantity'].min())
    # 5. Отфильтруйте значения, взяв только те, у которых category Товары для дома
    filtred_data = dataframe[dataframe['category'] == 'Товары для дома']
    result_dict = {
        'mean': round(mean,2),
        'max_value': max_value,
        'min_value': min_value,
    }
    return result_dict, dataframe


def task4():
    data_file = './55/fourth_task.txt'
    dataframe = get_dataframe(data_file)
    result_dict, dataframe = make_task(dataframe)
    save_file('Answers/task4_params.txt',result_dict)
    dataframe.to_csv('Answers/task4_endTable.txt')


if __name__ == "__main__":
    task4()