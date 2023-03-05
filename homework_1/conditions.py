from copy import deepcopy


class Condition:

    def __init__(self, feature: str, greater: bool, value: float):
        self.feature = feature
        self.greater = greater
        self.value = value

    def __add__(self, other: "Condition") -> "Condition" or "ConditionsGroup":
        if isinstance(other, Condition):
            if (self.feature == other.feature
                    and self.greater == other.greater):
                return Condition(
                    self.feature,
                    other.greater,
                    max(self.value, other.value) if self.greater
                    else min(self.value, other.value))
            else:
                return ConditionsGroup(self, other)
        else:
            raise ValueError('expected Condition')

    def merge_with_group(self, other: "ConditionsGroup") -> "ConditionsGroup":
        flag = False
        list_of_conditions = []
        if isinstance(other, ConditionsGroup):
            for index in range(len(other.conditions)):
                if isinstance(self + other.conditions[index], Condition):
                    list_of_conditions.append(self + other.conditions[index])
                    flag = True
                    break
                else:
                    list_of_conditions.append(other.conditions[index])
            if flag:
                return ConditionsGroup(*list_of_conditions)
            else:
                return ConditionsGroup(*list_of_conditions, self)
        else:
            raise ValueError('expected ConditionsGroup')


class ConditionsGroup:

    def __init__(self, *args):
        self.conditions = list(args)

    def __add__(self, other) -> "ConditionsGroup":
        if isinstance(other, ConditionsGroup):
            buf_conditions_group = deepcopy(other)
            print(buf_conditions_group.conditions)
            for condition in self.conditions:
                flag = True
                for index in range(len(buf_conditions_group.conditions)):
                    if isinstance(condition + buf_conditions_group.conditions[index], Condition):
                        buf_conditions_group.conditions[index] = condition + \
                                                                 buf_conditions_group.conditions[index]
                        flag = False
                        break
                if flag:
                    buf_conditions_group.conditions.append(condition)
            return buf_conditions_group
        else:
            raise ValueError('expected ConditionsGroup')


a = Condition('рост', True, 190)
b = Condition('рост', False, 180)
d = Condition('рост', True, 200)
e = Condition('рост', False, 200)
c = a + b
f = d + e
print(c.conditions, f.conditions)
v = c + f
print(v.conditions)
for cond in v.conditions:
    print(cond.value, cond.feature)