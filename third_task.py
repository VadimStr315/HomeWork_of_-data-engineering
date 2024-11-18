import os
import re
import csv
import math 

import requests
import pandas as pd


# сохранение в файл
def save_file(path, list_):
    with open(path, 'w', encoding='utf-8') as file:
        for item in list_:
            file.write(f"{item}\n")
    print('Saving True')


# чтение из файла
def read_csv(path):
    with open(path, mode='r', newline='') as file:
        reader = csv.reader(file)
        csv_data = [row[0] for row in reader]
        return csv_data


# преобразование строки в число
def str_to_int(data):
    new_list = list()
    for row in data:
        number_list_str = row.split()
        numbers = list()
        for index, num in enumerate(number_list_str):
            if num == 'N/A':
                new_num = (int(number_list_str[index-1])+int(number_list_str[index+1]))/2
                numbers.append(new_num)
            else:
                numbers.append(int(num))
        new_list.append(numbers)
    return new_list


# сортировка
def sorted_data(data):
    for index, row in enumerate(data):
        data[index] = sorted(row, key=lambda x: (x % 3 != 0, x))
    return data


# получение суммы
def get_sum(data):
    result = list()
    for row in data:
        result.append(sum(row))
    return result


def task3():
    data = read_csv('55/third_task.txt')
    data = str_to_int(data)
    data = sorted_data(data)
    result = get_sum(data)
    save_file('Answers/task3.txt',result)


if __name__ == "__main__":
    task3()