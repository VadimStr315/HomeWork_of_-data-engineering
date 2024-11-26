import os
import re
import csv
import math 

import requests
import pandas as pd


def get_dataframe(path):
    dataframe = pd.read_html(path, encoding='utf-8')[0]
    return dataframe   


def task5():
    data_file = './55/fifth_task.html'
    dataframe = get_dataframe(data_file)
    dataframe.to_csv("Answers/task5.txt")


if __name__ == "__main__":
    task5()