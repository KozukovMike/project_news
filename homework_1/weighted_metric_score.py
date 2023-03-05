from typing import List, Callable
from Gini_score import gini_score as mt


def weighted_metric_score(metric: Callable, *args: List) -> float:
    total_length = sum(list(map(lambda x: len(x), args)))
    total_value = 0
    for items in args:
        value_of_metric = metric(items)
        total_value += value_of_metric * len(items) / total_length
    return total_value


print('result: ', weighted_metric_score(mt, [1, 1, 2, 1, 3, 2], [3, 3, 2]))
