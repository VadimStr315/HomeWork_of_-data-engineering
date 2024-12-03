import xml.etree.ElementTree as ET
import json
import os

import pandas as pd


def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    clothing_items = []
    
    for clothing in root.findall('clothing'):
        item_data = {
            "id": clothing.find('id').text.strip() if clothing.find('id') is not None else None,
            "name": clothing.find('name').text.strip() if clothing.find('name') is not None else None,
            "category": clothing.find('category').text.strip() if clothing.find('category') is not None else None,
            "size": clothing.find('size').text.strip() if clothing.find('size') is not None else None,
            "color": clothing.find('color').text.strip() if clothing.find('color') is not None else None,
            "material": clothing.find('material').text.strip() if clothing.find('material') is not None else None,
            "price": int(clothing.find('price').text.strip()) if clothing.find('price') is not None else None,
            "rating": float(clothing.find('rating').text.strip()) if clothing.find('rating') is not None else None,
            "reviews": int(clothing.find('reviews').text.strip()) if clothing.find('reviews') is not None else None,
            "exclusive": clothing.find('exclusive').text.strip() if clothing.find('exclusive') is not None else None,
            "sporty": clothing.find('sporty').text.strip() if clothing.find('sporty') is not None else None,
            "new": clothing.find('new').text.strip() if clothing.find('new') is not None else None,
        }
        clothing_items.append(item_data)
    
    return clothing_items


def get_xml_files(folderpath):
    data = list()
    for filename in os.listdir(folderpath):
        if filename.endswith('.xml'):
            file_path = os.path.join(folderpath, filename)
            clothing_data = parse_xml_file(file_path)
            data.extend(clothing_data)
    return data


def convert_to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)


def sort_data(data, field):
    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by=field)
    return sorted_df.to_dict(orient='records')


def filter_data(data, field, value):
    return [item for item in data if item.get(field) == value]


def calculate_statistics(data, numeric_field):
    df = pd.DataFrame(data)
    return {
        "sum": df[numeric_field].sum(),
        "min": df[numeric_field].min(),
        "max": df[numeric_field].max(),
        "average": df[numeric_field].mean()
    }


def calculate_frequency(data, text_field):
    df = pd.DataFrame(data)
    return df[text_field].value_counts().to_dict()


def get_xml_files(folderpath):
    data = list()
    
    for filename in os.listdir(folderpath):
        if filename.endswith('.xml'):
            file_path = os.path.join(folderpath, filename)
            clothing_data = parse_xml_file(file_path)
            data.extend(clothing_data)

    return data


def fourth_data(folderpath):
    data = get_xml_files(folderpath)

    json_data = convert_to_json(data)
    print("Json:\n", json_data)

    sorted_items = sort_data(data, 'price')
    print("Сортировке по цене\n", convert_to_json(sorted_items))

    filtered_items = filter_data(data, 'category', 'Blouse')
    print("Фильтрация по категории 'Blouse':\n", convert_to_json(filtered_items))

    price_stats = calculate_statistics(data, 'price')
    print("Статистика по столбцу 'Цена':\n", price_stats)

    color_freq = calculate_frequency(data, 'color')
    print("Часота столбца цвета:\n", color_freq)


if __name__ == "__main__":
    fourth_data()