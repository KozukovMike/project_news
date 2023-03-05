import random
from typing import List


input_list = [random.randint(1, 3) for i in range(20)]


def gini_score(items: List[int]) -> float:
    length = len(items)
    p = 0
    while len(items) > 0:
        current_length = len(items)
        current_item = items[0]
        items = list(filter(lambda x: x != current_item, items))
        p += ((current_length - len(items)) / length)**2
    return round(1 - p, 3)


