import numpy as np


point_1 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
point_2 = np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]])
print(np.square(point_2 - point_1))


def euclidean_distance(XA: np.ndarray, XB: np.ndarray) -> np.ndarray:
    return np.array([[np.sqrt(np.sum(np.square(i - j))) for i in XA] for j in XB])


print(euclidean_distance(point_2, point_1))
