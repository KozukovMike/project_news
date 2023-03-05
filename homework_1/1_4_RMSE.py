from typing import List, Union


inp = [-0.1, -2.0, 1.0, 1.8, 0.8]


def rmse_score(items: List[Union[float, int]]) -> float:
    total = 0
    for i in items:
        total += (sum(items) / len(items) - i)**2
    return (total / len(items))**0.5


print(rmse_score(inp))
