from typing import List, Tuple, Iterable, Union


T = [1, 1, 2, 2, 1, 1, 2, 1, 3, 1, 3, 4, 1]
F = [3, 1, 9, 9, 1, 5, 2, 1, 7, 1, 3, 4, 9]


def split_target_by_feature(targets: List, features: List, split_value: Union[int, float]) -> Tuple[Iterable, Iterable]:
    just_buf = sorted(list(zip(targets, features)), key=lambda x: x[1])
    ind_in_sorted_f_of_split_value = ~sorted(features, reverse=True).index(split_value)
    less_part = [just_buf[i][0] for i in range(-len(just_buf), ind_in_sorted_f_of_split_value + 1)]
    more_part = [just_buf[i][0] for i in range(ind_in_sorted_f_of_split_value + 1, 0)]
    return less_part, more_part


print(split_target_by_feature(T, F, 5))
