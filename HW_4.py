"""
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
"""

import requests
from lxml import html
from fake_headers import Headers
import datetime
import pandas as pd


def rus_news():
    header = Headers(headers=True).generate()

    url_l = 'https://lenta.ru/'
    url_ya = 'https://yandex.ru/news/'

    response_l = requests.get(url_l, headers=header)
    response_ya = requests.get(url_ya, headers=header)

    parsed_l = html.fromstring(response_l.text)
    parsed_ya = html.fromstring(response_ya.text)

    name = []
    news_date = []
    news_link = []
    source = []
    # парсинг lenta.ru
    for i in range(2, 12):
        try:
            p = '//*[@id="root"]/section[2]/div/div/div[2]/div[1]/section/div/div[' + str(i) + ']/a'
            name.extend(parsed_l.xpath(p + '/text()'))
            link = parsed_l.xpath(p + '/@href')[0]

            spl = link.split('/')
            news_date.append(datetime.date(int(spl[2]), int(spl[3]), int(spl[4])))
            news_link.append('https://lenta.ru' + link)
            source.append('Lenta.ru')
        except IndexError:
            continue
    # парсинг Yandex News
    for i in range(1, 6):
        if i == 1:
            p_ya = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[1]/article/div[2]/a'
            p_date_ya = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[1]/article/div[2]/div[2]/div[1]/div/span[2]'
        else:
            p_ya = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[' + str(i) + ']/article/div[1]/div/a'
            p_date_ya = '//*[@id="neo-page"]/div/div[2]/div/div[1]/div[1]/div[' + str(i) + ']/article/div[3]/div[1]/div/span[2]'

        name.extend(parsed_ya.xpath(p_ya + '/h2/text()'))
        news_link.extend(parsed_ya.xpath(p_ya + '/@href'))
        news_date.extend(parsed_ya.xpath(p_date_ya + '/text()'))
        source.append('Yandex News')

    df_dict = {'Название новости': name, 'Ссылка': news_link, 'Дата': news_date, 'Источник': source}
    df = pd.DataFrame(df_dict)
    df.to_csv('News.csv')
    print('Done')
    return df


print(rus_news())
