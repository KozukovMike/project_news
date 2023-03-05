import math
from typing import List


def entropy_score(items: List[int]) -> float:
    length = len(items)
    total = 0
    while len(items) > 0:
        current_length = len(items)
        current_item = items[0]
        items = list(filter(lambda x: x != current_item, items))
        total += (current_length - len(items)) / length * math.log2((current_length - len(items)) / length)
    return round(-total, 3)
