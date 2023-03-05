import math
from typing import List, Callable


T = [1, 1, 2, 2, 1, 1, 3, 1, 3, 1, 3, 4, 1]
F = [3, 1, 9, 9, 1, 5, 2, 1, 7, 1, 3, 4, 9]
F1 = [3, 1, 9, 9, 1, 1, 2, 1, 7, 1, 3, 4, 9]
F2 = [3, 1, 9, 9, 1, 1, 1, 1, 7, 1, 3, 4, 9]
F3 = [3, 1, 9, 9, 1, 5, 2, 1, 1, 1, 3, 4, 9]


def choose_score_func(score_func: Callable):

    def split_target_by_feature(targets: List, options: List[List]):
        result_list = []
        for i, features in enumerate(options):
            t_and_f = sorted(list(zip(targets, features)), key=lambda x: x[1])
            unique_values = set(features)
            current_list_of_values = []
            for split_value in unique_values:
                ind_in_sorted_f_of_split_value = ~sorted(features, reverse=True).index(split_value)
                less_part = [t_and_f[i][0] for i in range(-len(t_and_f), ind_in_sorted_f_of_split_value + 1)]
                more_part = [t_and_f[i][0] for i in range(ind_in_sorted_f_of_split_value + 1, 0)]
                total = (score_func(less_part)*len(less_part)/len(features) +
                         score_func(more_part)*len(more_part)/len(features))
                current_list_of_values.append((total, split_value, i))
            result_list.append(min(current_list_of_values, key=lambda x: x[0]))
        return options[min(result_list, key=lambda x: x[0])[2]], min(result_list, key=lambda x: x[0])[1]
    return split_target_by_feature


@choose_score_func
def gini_score(items: List[int]) -> float:
    length = len(items)
    p = 0
    while len(items) > 0:
        current_length = len(items)
        current_item = items[0]
        items = list(filter(lambda x: x != current_item, items))
        p += ((current_length - len(items)) / length)**2
    return round(1 - p, 3)


@choose_score_func
def entropy_score(items: List[int]) -> float:
    length = len(items)
    total = 0
    while len(items) > 0:
        current_length = len(items)
        current_item = items[0]
        items = list(filter(lambda x: x != current_item, items))
        total += (current_length - len(items)) / length * math.log2((current_length - len(items)) / length)
    return round(-total, 3)


answer_gini = gini_score(T, [F, F1, F2, F3])
print('for gini:', answer_gini)
answer_entropy = entropy_score(T, [F, F1, F2, F3])
print('for entropy:', answer_entropy)
