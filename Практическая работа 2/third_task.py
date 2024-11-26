import json
import msgpack
import os


def third_task():
    with open('./55/third_task.json', 'r',encoding='utf-8') as json_file:
        products = json.load(json_file)

    aggregated_info = list()

    for product in products:
        prices = product.get('prices', [])
        
        if prices:
            average_price = sum(prices) / len(prices)
            max_price = max(prices)
            min_price = min(prices)
        else:
            average_price = None  
            min_price = None
            max_price = None

        aggregated_info.append({
            'average_price': average_price,
            'max_price': max_price,
            'min_price': min_price
        })

    with open('Answers/third_task_aggregated_info.json', 'w') as json_out:
        json.dump(aggregated_info, json_out, indent=4)

    with open('Answers/third_task_aggregated_info.msgpack', 'wb') as msgpack_out:
        msgpack.pack(aggregated_info, msgpack_out)

    size_json = os.path.getsize('Answers/third_task_aggregated_info.json')
    size_msgpack = os.path.getsize('Answers/third_task_aggregated_info.msgpack')

    print(f"Размер third_task_aggregated_info.json: {size_json} bytes")
    print(f"Размер third_task_aggregated_info.msgpack: {size_msgpack} bytes")


if __name__ == "__main__":
    third_task()