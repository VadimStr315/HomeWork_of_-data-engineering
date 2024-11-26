import json
import numpy as np


def save_first_data(data):
    with open('Answers/first_task.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Results have been written to results.json")


def first_task():

    matrix =  np.load('./55/first_task.npy')

    total_sum = float(np.sum(matrix))
    arithmetic_mean = float(np.mean(matrix))

    main_diagonal = np.diagonal(matrix)
    main_diagonal_sum = float(np.sum(main_diagonal))
    main_diagonal_mean = float(np.mean(main_diagonal))

    secondary_diagonal = np.diagonal(np.fliplr(matrix))
    secondary_diagonal_sum = float(np.sum(secondary_diagonal))
    secondary_diagonal_mean = float(np.mean(secondary_diagonal))

    max_value = float(np.max(matrix))
    min_value = float(np.min(matrix))

    results = {
        "sum": total_sum,
        "avr": arithmetic_mean,
        "sumMD": main_diagonal_sum,
        "avrMD": main_diagonal_mean,
        "sumSD": secondary_diagonal_sum,
        "avrSD": secondary_diagonal_mean,
        "max_value": max_value,
        "min_value": min_value
    }
    
    save_first_data(results) 


if __name__ == "__main__":
    first_task()