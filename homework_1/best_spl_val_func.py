from typing import List, Callable, Union
from Entropy import entropy_score


T = [1, 1, 2, 2, 1, 1, 3, 1, 3, 1, 3, 4, 1]
F = [3, 1, 9, 9, 1, 5, 2, 1, 7, 1, 3, 4, 9]


def split_target_by_feature(score_func: Callable, targets: List, features: List) -> Union[int, float]:
    t_and_f = sorted(list(zip(targets, features)), key=lambda x: x[1])
    unique_values = set(features)
    result_list = []
    for split_value in unique_values:
        ind_in_sorted_f_of_split_value = ~sorted(features, reverse=True).index(split_value)
        less_part = [t_and_f[i][0] for i in range(-len(t_and_f), ind_in_sorted_f_of_split_value + 1)]
        more_part = [t_and_f[i][0] for i in range(ind_in_sorted_f_of_split_value + 1, 0)]
        total = (score_func(less_part)*len(less_part)/len(features) +
                 score_func(more_part)*len(more_part)/len(features))
        result_list.append((total, split_value))
    return min(result_list, key=lambda x: x[0])[1]


print(split_target_by_feature(entropy_score, T, F))
