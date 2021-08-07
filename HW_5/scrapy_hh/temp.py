# import requests
# from lxml import html
# from fake_headers import Headers
#
#
#
#
# header = Headers(headers=True).generate()
#
#
# url_l = 'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Бухгалтер&from=suggest_post&page=1'
#
# response = requests.get(url_l, headers=header)
#
#
# parsed_l = html.fromstring(response.text)
# p = parsed_l.css('div.bloko-gap_top span.bloko-form-spacer a.bloko-button::attr(href)').extract()
# print(p)
import pickle
sal = ["200 000250 000 руб.месяц", "от 1000 до 2000 USD", "По договорённости",
       "от 150 000 руб.месяц", "12 000 руб.месяц", "до 90 000 руб.месяц"]

with open('outfile', 'rb') as fp:
    sallist = pickle.load(fp)

sal = sallist[4:]
print(sal)
def cut_the_sal(sal_list):
    """
    Метод "разбивания" зарплаты на минимальную, максимальную и валюту
    """
    n = len(sal_list)
    if n == 1:
        min_sal = 'Nan'
        max_sal = 'Nan'
        curr = 'Nan'
    elif n == 5:
        min_sal = ''.join(sal_list[0])
        max_sal = ''.join(sal_list[1])
        curr = ''.join(sal_list[3])
    else:

        if sal_list[0] == 'от':
            sal_ = sal_list[2].rsplit('0', maxsplit=1)

            min_sal = sal_[0] + str(0)
            max_sal = 'Nan'
            curr = sal_[1]
        elif sal_list[0] == 'до':
            sal_ = sal_list[2].rsplit('0', maxsplit=1)
            max_sal = sal_[0] + str(0)
            min_sal = 'Nan'
            curr = sal_[1]
        else:
            max_sal = sal_list[0]
            min_sal = sal_list[0]
            curr = sal_list[2]
    return min_sal, max_sal, curr

for s in sal:
    print(cut_the_sal(s))

# lst = '15000руб.'
# s = lst.rsplit('0', maxsplit=1)
# print(s)