import pandas as pd
import json
import pickle


def fourth_task():
    with open('55/fourth_task_products.json', 'rb') as pkl_file:
        products = pickle.load(pkl_file)

    with open('55/fourth_task_updates.json', 'r',encoding='utf-8') as json_file:
        price_updates = json.load(json_file)

    for update in price_updates:
        product_name = update['name']
        method = update['method']
        param = update['param']

        for product in products:
            if product['name'] == product_name:
                if method == "add":
                    product['price'] += param
                elif method == "sub":
                    product['price'] -= param
                elif method == "percent+":
                    product['price'] *= (1 + param)
                elif method == "percent-":
                    product['price'] *= (1 - param)


    with open('Answers/fourth_task_modified_products.pkl', 'wb') as modified_pkl_file:
        pickle.dump(products, modified_pkl_file)

    print("Данные сохранены в fourth_task_modified_products.pkl")


if __name__ == "__main__":
    fourth_task()