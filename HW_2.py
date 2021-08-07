"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input
или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии (например, работодателя
и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести
с помощью dataFrame через pandas.
"""

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup as Bs
import lxml
import pandas as pd


def cut_the_sal(sal_list):
    """
    Функция "разбивания" зарплаты на минимальную и максимальную
    :param sal_list:
    :return:
    """
    min_sal = []
    max_sal = []
    for sal in sal_list:
        if sal == 'По договорённости' or sal == '':
            min_sal.append('-1')
            max_sal.append('-1')
        else:
            sal_1 = sal.rsplit('руб.')[0]
            if sal_1[:2] == 'от':
                min_sal.append(sal_1[2:])
                max_sal.append('10000000')
            elif sal_1[:2] == 'до':
                min_sal.append(0)
                max_sal.append(sal_1[2:])
            else:
                sal_2 = sal_1.rsplit('—')
                if len(sal_2) == 1:
                    sal_2 = sal_2[0].rsplit(' – ')
                if len(sal_2) > 1:
                    min_sal.append(sal_2[0])
                    max_sal.append(sal_2[1])
                else:
                    min_sal.append(sal_2[0])
                    max_sal.append(sal_2[0])
    return min_sal, max_sal


def page_info(url1, url2):
    """
    Функция парсинга одной страницы с вакансиями
    :param url1:
    :param url2:
    :return:
    """
    header = Headers(headers=True).generate()
    response1 = requests.get(url1, headers=header) # SuperJob
    response2 = requests.get(url2, headers=header) # HeadHunter
    soup = Bs(response1.text, 'lxml')
    soup_hh = Bs(response2.text, 'lxml')

    # Название вакансии
    sj_name = [i.text for i in soup.find_all(class_='_1h3Zg _2rfUm _2hCDz _21a7u')]
    hh_name = [i.text for i in soup_hh.find_all(class_='resume-search-item__name')]

    # Уровень зарплаты
    sal = [i.text.replace('\xa0', '') for i in soup.find_all(class_='_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW')]
    sj_sal = cut_the_sal(sal)
    sal2 = []
    for num, i in enumerate(soup_hh.find_all(class_='vacancy-serp-item__row vacancy-serp-item__row_header')):
        sal2.append(i.text.replace('\u202f', '').replace(hh_name[num], ''))
    hh_sal = cut_the_sal(sal2)

    # Название компании
    sj_org = []
    for i in soup.find_all(class_='_3_eyK _3P0J7 _9_FPy'):
        try:
            sj_org.append(i.select_one('a').text)
        except AttributeError:
            sj_org.append('No data')
    hh_org = [i.text.replace('\xa0', '') for i in soup_hh.find_all(class_='vacancy-serp-item__meta-info-company')]

    # Ссылка
    sj_link = ['https://www.superjob.ru' + i.select_one('a')['href'] for i in soup.find_all(class_='_1h3Zg _2rfUm _2hCDz _21a7u')]
    hh_link = []
    for i in soup_hh.find_all(class_='g-user-content'):
        try:
            hh_link.append(i.select_one('a')['href'])
        except TypeError:
            continue

    df_dict = {'Вакансия': sj_name + hh_name, 'Компания': sj_org + hh_org, 'Мин зарплата': sj_sal[0] + hh_sal[0],
               'Макс зарплата': sj_sal[1] + hh_sal[1], 'Сайт': ['SuperJob'] * len(sj_name) + ['HeadHunter'] * len(hh_name),
               'Ссылка': sj_link + hh_link}
    df = pd.DataFrame(df_dict)
    return df


def vacancy_search(vac='Главный бухгалтер', pages=3):
    """
    Функция сбора данных о заданных вакансиях с SuperJob и HeadHunter
    :param vac:
    :param pages:
    :return:
    """
    n = 1
    data = pd.DataFrame(columns=['Вакансия', 'Компания', 'Мин зарплата', 'Макс зарплата', 'Сайт', 'Ссылка'])
    while n <= pages:
        if n == 1:
            url_sj = 'https://www.superjob.ru/vacancy/search/?keywords=' + str('%20'.join(vac.split())) + '&geo%5Bt%5D%5B0%5D=4'
            url_hh = 'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=' + str('+'.join(vac.split()))
        else:
            url_sj = 'https://www.superjob.ru/vacancy/search/?keywords=' + str(
                '%20'.join(vac.split())) + '&geo%5Bt%5D%5B0%5D=4&page=' + str(n)
            url_hh = 'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=' + \
                     str('+'.join(vac.split())) + '&page=' + str(n-1)
        data = pd.concat([data, page_info(url_sj, url_hh)], ignore_index=True)
        n += 1

    data.to_csv('Vacancy.csv')
    print('Done')
    return data


result = vacancy_search()
print(result)
