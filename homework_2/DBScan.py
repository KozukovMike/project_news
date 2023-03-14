import sqlite3
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from numpy.random import default_rng
from typing import Union, Dict, Iterable, List


class DBScan:

    def __init__(self, points: np.array):
        self.points = points
        self.visited: np.ndarray = []
        self.groups: Dict[str: np.ndarray] = {}
        self.__distance = pd.DataFrame(data=cdist(self.points, self.points))
        self.not_visited: np.ndarray = list(self.__distance.index)

    def get_random_point(self):
        point = np.random.choice(self.not_visited, 1)
        index = self.not_visited.index(point)
        del self.not_visited[index]
        return point[0]

    def make_groups(self, e: float, n: int):

        def recursive_getting_points(df: pd.DataFrame, start_list: Iterable, point_list: Union[List, np.array]):
            for point_ in start_list:
                if point_ not in point_list and len(np.where(df.loc[point_, :] == True)[0]) != 1:
                    point_list.append(point_)
                    current_points = np.where(df.loc[point_, :] == True)[0]
                    point_list = recursive_getting_points(df, set(current_points) - set(point_list), point_list)
                elif point_ not in point_list:
                    point_list.append(point_)
            return point_list

        bool_df = self.__distance.apply(lambda x: x < e)
        i = 0
        while len(self.not_visited):
            point = self.get_random_point()
            list_op_points = [point]
            list_of_indexes = np.where(bool_df.loc[point, :] == True)[0]
            points_of_group = recursive_getting_points(bool_df, list_of_indexes, list_op_points)
            self.not_visited = list(set(self.not_visited) - set(points_of_group))
            if len(points_of_group) > n:
                self.groups[f'{i}'] = points_of_group
            else:
                self.groups[f'outlier {i}'] = points_of_group
            i += 1

        return self.groups


sql_tour = """
SELECT id, first_name, last_name, age, lat, lng
FROM
    tourists INNER JOIN zip_codes ON
    tourists.zip = zip_codes.zip
ORDER BY id
;"""
sql_restaurants = """
SELECT id, type, lat, lng
FROM 
	restaurants INNER JOIN zip_codes ON
	restaurants.zip = zip_codes.zip 
ORDER BY id
;"""
con = sqlite3.Connection("data/hw2.sqlite")
restaurants = pd.read_sql(sql=sql_restaurants, con=con)
tourists = pd.read_sql(sql=sql_tour, con=con)
restaurants = restaurants.drop(['type', 'id'], axis=1)
tourists = tourists.drop(['last_name', 'first_name', 'age', 'id'], axis=1)
a = cdist(restaurants, restaurants)
u = DBScan(restaurants)
d = u.make_groups(0.05, 5)

