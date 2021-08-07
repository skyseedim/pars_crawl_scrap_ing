import scrapy
from scrapy.http import HtmlResponse
from HWs.HW_5.scrapy_hh.scrapy_job.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']
    custom_settings = {'DEPTH_LIMIT': 3}


    def parse(self, response: HtmlResponse):
        next_page = response.css(
            'div.bloko-gap_top span.bloko-form-spacer a.bloko-button::attr(href)'
        ).extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

        for links in vacansy:
            yield response.follow(links, callback=self.vacansy_parse)


    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1::text').extract_first()
        salary = response.css(
            'div.vacancy-title p.vacancy-salary span.bloko-header-2::text'
        ).extract()[0].replace('\xa0', '')
        sal = self.cut_the_sal(salary)
        salary_min = sal[0]
        salary_max = sal[1]
        currency = sal[2]
        source = 'HeadHunter'
        link = response.url
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, currency=currency, source=source, link=link)


    def cut_the_sal(self, salary):
        """
        Метод "разбивания" зарплаты на минимальную, максимальную и валюту
        """
        if salary == "з/п не указана":
            min_sal = 'Nan'
            max_sal = 'Nan'
            curr = 'Nan'
        elif salary[:2] == "до":
            min_sal = 'Nan'
            sal = salary[3:].rsplit(' ')
            max_sal = sal[0]
            curr = sal[1]
        else:
            sal = salary[3:].rsplit(' ')
            min_sal = sal[0]
            curr = sal[-1]
            if len(sal) == 2:
                max_sal = 'Nan'
            else:
                max_sal = sal[2]
        return min_sal, max_sal, curr
