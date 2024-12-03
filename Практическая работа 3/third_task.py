import json
import os
import xml.etree.ElementTree as ET

import pandas as pd


def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    star_data = {
        "name": root.find('name').text.strip(),
        "constellation": root.find('constellation').text.strip(),
        "spectral_class": root.find('spectral-class').text.strip(),
        "radius": int(root.find('radius').text.strip()),
        "rotation": root.find('rotation').text.strip(),
        "age": root.find('age').text.strip(),
        "distance": float(root.find('distance').text.strip().split()[0]),
        "absolute_magnitude": float(root.find('absolute-magnitude').text.strip().split()[0])
    }
    return star_data


def convert_to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)


def sort_data(data, field):
    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by=field)
    return sorted_df.to_dict(orient='records')


def filter_data(data, field, value):
    return [item for item in data if item[field] == value]


def calculate_statistics(data, numeric_field):
    df = pd.DataFrame(data)
    return {
        "sum": df[numeric_field].sum(),
        "min": df[numeric_field].min(),
        "max": df[numeric_field].max(),
        "average": df[numeric_field].mean()
    }


def label_frequency(data, text_field):
    df = pd.DataFrame(data)
    return df[text_field].value_counts().to_dict()


def get_xml_files(folderpath):
    data = list()
    for filename in os.listdir(folderpath):
        if filename.endswith('.xml'):
            file_path = os.path.join(folderpath, filename)
            star_data = parse_xml_file(file_path)
            data.append(star_data)
    return data


def third_task(folderpath):
    data = get_xml_files(folderpath)
    
    json_data = convert_to_json(data)
    print("JSON Data:\n", json_data)

    sorted_data= sort_data(data, 'radius')
    print("Сортировка по radius:\n", convert_to_json(sorted_data))

    filtered_data = filter_data(data, 'constellation', 'Близнецы')
    print("Фильтрация по Constellation:\n", convert_to_json(filtered_data))

    statistic_data = calculate_statistics(data, 'radius')
    print("Статистика по Radius:\n", statistic_data)

    constellation_freq = label_frequency(data, 'constellation')
    print("Частота по constellation:\n", constellation_freq)


if __name__ == "__main__":
    third_task('./55/3')