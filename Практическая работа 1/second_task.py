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
            if k == "sums":
                for value in v:
                    file.write(f"{value}\n")
            elif k =='max_num':
                file.write(f"\n{value}\n")
            elif k =='min_num':
                file.write(f"\n{value}\n")
    print('Saving True')


# чтение csv
def read_csv(path):
    with open(path, mode='r', newline='') as file:
        reader = csv.reader(file)
        csv_data = [row[0] for row in reader]
        return csv_data
    

# преобразование строк в число
def str_to_int(data):
    new_list = list()
    for row in data:
        number_list_str = row.split()
        new_list.append(list(map(int, number_list_str)))
    return new_list


# получение суммы корней
def get_sqrt_sums(data):
    sum_list = list()
    for row in data:
        positive_sqrt = [math.sqrt(num) for num in row if num > 0]
        sum_of_sqrt = round(sum(positive_sqrt))
        sum_list.append(sum_of_sqrt)
    return sum_list


# основная функция
def task2():
    data = read_csv('55\second_task.txt')
    data = str_to_int(data)
    result = get_sqrt_sums(data)
    min_num = min(result)
    max_num = max(result)
    result_dict = {
        "sums": result,
        'max_num':max_num,
        'min_num':min_num}
    
    save_file('Answers/task2.txt',result_dict)


if __name__ == '__main__':
    task2()