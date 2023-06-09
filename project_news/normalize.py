import pandas as pd
import numpy as np
import pymorphy3
from datetime import date, datetime


def normalize(x: str) -> list:
    '''
    приводит любую строку к списку слов, создано для того чтобы в последствии искать нужное слово
    :param x: строка на вход
    :return: список слов в строке
    '''

    morph = pymorphy3.MorphAnalyzer()
    list_of_words = x.split()
    norm_list_of_words = [morph.parse(word)[0].normal_form for word in list_of_words]
    return norm_list_of_words


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    функция нормализует(применяет к каждой новости функцию normalize) новости каждый день.
    То есть она нормализует новости только сегодняшнего дня
    :param df: датафрейм с новостями
    :return: записывает в файл нормализованный датафрейм и возвращает его
    '''

    today = datetime.today()
    today = today.strftime('%Y-%m-%d')
    n = pd.read_csv('C:/Users/mike/PycharmProjects/parsing/my_dataframe.csv')
    df.loc[df['date'] == today, 'title'] = \
        df.loc[df['date'] == today, 'title'].apply(lambda x: normalize(x))
    df_norm = pd.concat([n, df.loc[df['date'] == today]])
    df_norm.to_csv('C:/Users/mike/PycharmProjects/parsing/my_dataframe.csv', index=False)
    return df_norm


def df_where_word_in(df: pd.DataFrame, word: str) -> pd.DataFrame:
    '''
    функция находит строки с новостями в датафрейм, где содержится слово, которое ищут
    :param df: наш датафрейм
    :param word: слово для поиска
    :return: датафрейм
    '''

    df_copy = df.copy()
    df_copy['title'] = df_copy['title'].apply(lambda x: word in x)
    current_ind = np.where(df_copy['title'] == True)
    df_copy = df.loc[current_ind].copy()
    return df_copy
