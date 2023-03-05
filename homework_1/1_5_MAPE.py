from typing import List, Union


inp = [-0.1, -2.0, 1.0, 1.8, 0.8]


def mape_score(items: List[Union[float, int]]) -> float:
    total = 0
    items = list(filter(lambda x: x, items))
    for i in items:
        total += abs((sum(items) / len(items) - i) / i)
    return 100 * total / len(items)


print(mape_score(inp))
