# Для данного задания был взять датасет с Kaggle 
# https://www.kaggle.com/datasets/mariusborel/electric-vhicule-population-data?resource=download 
# весом 50 МБ
import json
import os

import pandas as pd
import msgpack
import kagglehub

# Download latest version


def file_sizes():
    file_sizes = {
    'CSV Size': os.path.getsize('Answers/fifth_task_dataset.csv'),
    'JSON Size': os.path.getsize('Answers/fifth_task_dataset.json'),
    'MsgPack Size': os.path.getsize('Answers/fifth_task_dataset.msgpack'),
    'PKL Size': os.path.getsize('Answers/fifth_task_dataset.pkl')
    }

    print("File Sizes (in bytes):")
    for format, size in file_sizes.items():
        print(f"{format}: {size}")



def count_stats(df):
    selected_fields = ['VIN (1-10)',
                       'County','City',
                       'State',
                       'Postal Code',
                       'Model Year',
                       'Make',
                       'Model',
                       'Electric Vehicle Type',
                       'Clean Alternative Fuel Vehicle (CAFV) Eligibility',
                       'Electric Range']
    numerical_fields = ['Postal Code', 'Model Year', 'Electric Range'] 
    categorical_fields = ['VIN (1-10)',
                          'County',
                          'City',
                          'State',
                          'Make',
                          'Model',
                          'Electric Vehicle Type',
                          'Clean Alternative Fuel Vehicle (CAFV) Eligibility']
    
    df_selected = df[selected_fields]
    statistics = {}

    for field in numerical_fields:
        statistics[field] = {
            'max': float(df_selected[field].max()),
            'min': float(df_selected[field].min()),
            'mean': float(df_selected[field].mean()),
            'sum': float(df_selected[field].sum()),
            'std_dev': float(df_selected[field].std())
        }

    for field in categorical_fields:
        statistics[field] = df_selected[field].value_counts().to_dict()

    return df_selected, statistics


def fifth_task():
    file_path = '55/Electric_Vehicle_Population_Data.csv'
    df = pd.read_csv(file_path)

    df_selected, statistics = count_stats(df)

    with open('Answers/fifth_task_statistics.json', 'w', encoding='utf-8') as json_file:
        json.dump(statistics, json_file, ensure_ascii=False, indent=4)

    df_selected.to_csv('Answers/fifth_task_dataset.csv', index=False)
    df_selected.to_json('Answers/fifth_task_dataset.json', orient='records', lines=True)
    df_selected.to_pickle('Answers/fifth_task_dataset.pkl')

    df_dict = df_selected.to_dict()
    with open('Answers/fifth_task_dataset.msgpack', 'wb') as msgpack_out:
        msgpack.pack(df_dict, msgpack_out)

    file_sizes()


if __name__ == "__main__":
    fifth_task()