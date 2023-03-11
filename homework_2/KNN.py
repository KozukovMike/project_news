import sqlite3
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


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


def knn(base: np.ndarray, entities: np.ndarray, ax_0: int, ax_1: int) -> np.ndarray:
    return pd.DataFrame(data=np.argsort(cdist(base, entities), axis=1)[:ax_0, :ax_1])


a = knn(tourists, restaurants, 3, 5)
print(a)
