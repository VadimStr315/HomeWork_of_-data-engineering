import os
import re
import csv
import math 

import requests
import pandas as pd


# чтение из файла
def read_file(path):
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
    return lines


# сохранение в файл основное задание
def save_file(path, word_counts):
    with open(path, 'w', encoding='utf-8') as file:
        for word, freq in word_counts.items():
            file.write(f"{word}:{freq}\n")
    print('Saving True')


# сохранение в файл по вариантам
def save_file_task1_2(path, list_):
    with open(path, 'w', encoding='utf-8') as file:
        for item in list_:
            file.write(f"{item}\n")
    print('Saving True')


# функция отчистки строки от спец. символов
def remove_symbols(input_string):
    symbols = "'!@#$%^&**().,/?/*;:`~\n"
    pattern = f"[{re.escape(symbols)}]"
    return re.sub(pattern, '', input_string)


# функция обработки списка строк
def modify_list(lines):
    modified_lines = [remove_symbols(line).replace('-',' ').lower() for line in lines]
    modified_lines_lists = [line.split(' ') for line in modified_lines]
    words_list = [word for line in modified_lines_lists for word in line]
    return words_list


# функция подсчета слов
def count_words(words_list):
    words = {}
    for word in set(words_list):
        if word not in words and word != '':        
            words[word] = words_list.count(word)
    sorted_dict = dict(sorted(words.items(), key=lambda item: item[1], reverse=True)) # сортировка слов
    return sorted_dict


# подсчет количества гласных
def count_vowels(string):
    vowels = 'aeiouy'  
    count = 0
    for char in string:
        if char in vowels:
            count += 1
    return count


# по вариантам
def by_variants():
    path = './55/first_task.txt'
    lines = read_file(path)
    modified_lines = modify_list(lines)
    modified_string = ''
    
    for word in modified_lines:
        modified_string+=word
    amount_vowels = count_vowels(modified_string)

    return [f'Количество букв в строке: {len(modified_string)}',
            f'Количество гласных букв в строке: {amount_vowels}',
            f'Доля гласных букв: {(amount_vowels*100)/len(modified_string):.2f} %']


# основная часть 
def task1():
    path = './55/first_task.txt'
    lines = read_file(path)
    modified_lines = modify_list(lines)
    result_dict = count_words(modified_lines)
    print(result_dict)
    save_file('Answers/task1_main.txt', result_dict)


#  по вариантам
def task1_2():
    data = by_variants()
    save_file_task1_2('Answers/task1_by_variants.txt',data)


if __name__ == "__main__":
   task1()
   task1_2()