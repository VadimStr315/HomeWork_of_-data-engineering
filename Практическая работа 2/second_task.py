import numpy as np
import os


def second_task():
    matrix = np.load('./55/second_task.npy')

    threshold = 555 #(500 + 55 вариант)

    indices = np.argwhere(matrix > threshold)

    x = indices[:, 0]
    y = indices[:, 1]
    z = matrix[indices[:, 0], indices[:, 1]]

    np.savez('Answers/second_task.npz', x=x, y=y, z=z)
    np.savez_compressed('Answers/second_task_compressed.npz', x=x, y=y, z=z)

    size_normal = os.path.getsize('Answers/second_task.npz')
    size_compressed = os.path.getsize('Answers/second_task_compressed.npz')

    print(f"Размер results.npz: {size_normal} bytes")
    print(f"Размер results_compressed.npz: {size_compressed} bytes")


if __name__ == "__main__":
    second_task()