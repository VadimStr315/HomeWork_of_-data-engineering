import os
import re
import csv
import math 

import requests
import pandas as pd


# отправка запроса 
def send_respone(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except ConnectionError:
        print('Error: connection error')
        return None
    

def task6():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    data = send_respone(url)
    df = pd.DataFrame(data['results'])
    df.to_html('Answers/task6.html')


if __name__ == "__main__":
    task6()