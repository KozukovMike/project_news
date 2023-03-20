import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from numpy.random import default_rng
from typing import Union


class Hello:

    def __init__(self, base: np.ndarray, entities: np.ndarray):
        self.base = pd.DataFrame(base)
        self.entities = pd.DataFrame(entities)

    def knn(self, ax_0: int, ax_1: int, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        if flag:
            return pd.DataFrame(data=np.argsort(cdist(self.base, self.entities), axis=1)[:ax_0, :ax_1])
        return np.argsort(cdist(self.base, self.entities), axis=1)[:ax_0, :ax_1]

    @staticmethod
    def get_random_centroids(amount_of_points: int, x: np.ndarray, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        if isinstance(x, np.ndarray):
            x = pd.DataFrame(data=x)
            x = x.sample(amount_of_points)
            if flag:
                return x
            return x.to_numpy()
        elif isinstance(x, pd.DataFrame):
            return x.sample(amount_of_points)

    def make_random_centroids(self, amount_of_points, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        rng = default_rng()
        data = {f'{i}': ((max(self.base[i]) - min(self.base[i])) * rng.random(amount_of_points) + min(self.base[i]))
                for i in self.entities.columns
                }
        df = pd.DataFrame(data=data)
        if flag:
            return pd.DataFrame(data=data)
        return df.to_numpy()

    def find_closest_centroids(self, centroids: np.ndarray, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        if flag:
            return pd.DataFrame(data=np.argsort(cdist(self.entities, centroids), axis=1)[:, :1])
        return np.argsort(cdist(self.entities, centroids), axis=1)[:, 0]

    def group_by_centroids_and_update(self, groups: np.ndarray, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        data = {f'{i}': [] for i in self.entities.columns}
        for point in set(groups):
            arr_of_ind_of_point = np.where(groups == point)
            current_entities = self.entities.iloc[arr_of_ind_of_point]
            average_of_columns = current_entities.mean()
            for i in average_of_columns.index:
                data[i].append(average_of_columns[i])
        res = pd.DataFrame(data=data)
        if flag:
            return res
        return res.to_numpy()

    def optimize_centroids(self, centroids: np.ndarray, flag: bool = False) -> Union[pd.DataFrame, np.ndarray]:
        while True:
            fig, ax = plt.subplots(figsize=(11, 5))
            _ = ax.scatter(x=self.entities["lat"], y=self.entities["lng"], s=10, c="firebrick", edgecolors="black",
                           linewidths=0.5, alpha=0.5)
            df = pd.DataFrame(centroids, columns=['lat', 'lng'])
            _ = ax.scatter(x=df["lat"], y=df["lng"], s=10, c="blue",
                           linewidths=3, alpha=1)
            plt.show()
            plt.close(fig)
            # print(pd.DataFrame(centroids, columns=['lat', 'lng']))
            groups = self.find_closest_centroids(centroids=centroids, flag=False)
            current_centroids = self.group_by_centroids_and_update(groups=groups, flag=False)
            # print(len(current_centroids))
            # если мы хотим добавить сентроиды(при условии что их стало меньше), если нет,
            # то просто убираем этот if и сентроидов будет меньше
            if len(centroids) != len(current_centroids):
                # print('enter')
                buf = self.make_random_centroids(len(centroids) - len(current_centroids), False)
                current_centroids = np.concatenate((current_centroids, buf))
            # print(len(current_centroids))
            # print(pd.DataFrame(centroids, columns=['lat', 'lng']))
            if np.array_equal(current_centroids, centroids):
                if flag:
                    return pd.DataFrame(data=current_centroids)
                return current_centroids
            centroids = current_centroids


sql_tour = """
SELECT lat, lng
FROM
    tourists INNER JOIN zip_codes ON
    tourists.zip = zip_codes.zip
ORDER BY id
;"""
sql_restaurants = """
SELECT lat, lng
FROM 
	restaurants INNER JOIN zip_codes ON
	restaurants.zip = zip_codes.zip 
ORDER BY id
;"""
con = sqlite3.Connection("data/hw2.sqlite")
restaurants = pd.read_sql(sql=sql_restaurants, con=con)
tourists = pd.read_sql(sql=sql_tour, con=con)
a = Hello(tourists, restaurants)
f = a.knn(3, 5)
print(f)
f = a.make_random_centroids(20, False)
print(f)
itog = a.optimize_centroids(f)
print(itog)
