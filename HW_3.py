"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""

import pandas as pd
from pymongo import MongoClient
import pprint


def load_data(data_path='Vacancy.csv', db_name='vacancy_db'):

    df = pd.read_csv(data_path, index_col=0, dtype='object')

    client = MongoClient('localhost', 27017)
    db = client[db_name]
    vac = db.vacancys_collection

    num = 0
    for i in range(len(df)):
        vac.insert_one({'name': df.iloc[i, 0], 'company': df.iloc[i, 1], 'min_sal': df.iloc[i, 2],
                        'max_sal': df.iloc[i, 3], 'site': df.iloc[i, 4], 'link': df.iloc[i, 5]})
        num += 1

    print(f'Data loaded | database name: {db_name} | number of loaded documents: {num}')


def find_sal(sal_threshold=100000, data_path='Vacancy.csv'):
    df = pd.read_csv(data_path, index_col=0)
    df[['Мин зарплата', 'Макс зарплата']] = df[['Мин зарплата', 'Макс зарплата']].apply(pd.to_numeric)

    lst = []
    for i in range(len(df)):
        if df.iloc[i, 3] == -1:
            continue
        elif df.iloc[i, 3] >= sal_threshold:
            lst.append(i)

    new_df = df.iloc[lst, :]
    print(new_df)
    return new_df


def new_vac(data_path='Vacancy.csv', db_name='vacancy_db'):
    df = pd.read_csv(data_path, index_col=0, dtype='object')

    client = MongoClient('localhost', 27017)
    db = client[db_name]
    vac = db.vacancys_collection

    for i in range(len(df)):
        vac.update_one(
            {'link': {'$ne': df.iloc[i, 5]}},
            {'$set': {'name': df.iloc[i, 0], 'company': df.iloc[i, 1], 'min_sal': df.iloc[i, 2],
             'max_sal': df.iloc[i, 3], 'site': df.iloc[i, 4], 'link': df.iloc[i, 5]}},
             upsert=True)


#load_data()
#new_vac()
