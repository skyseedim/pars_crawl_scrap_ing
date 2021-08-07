import scrapy
from scrapy.http import HtmlResponse
from HWs.HW_5.scrapy_hh.scrapy_job.items import JobparserItem


class SJSpider(scrapy.Spider):
    name = 'SuperJob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']
    custom_settings = {'DEPTH_LIMIT': 3}


    def parse(self, response: HtmlResponse):
        next_page = response.css(
            'div._31XDP div._3zucV a.icMQ_::attr(href)'
        ).extract()[-1]
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div._3zucV div.f-test-search-result-item div._1h3Zg a.icMQ_::attr(href)'
        ).extract()

        for links in vacansy:
            yield response.follow(links, callback=self.vacansy_parse)


    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1._1h3Zg::text').extract_first()

        salary = list(map(lambda x: x.replace('\xa0', ''), response.css(
            'div._3MVeX span._1OuF_ span._1h3Zg::text'
        ).extract()))
        salary_list = self.cut_the_sal(salary)
        salary_min = salary_list[0]
        salary_max = salary_list[1]
        currency = salary_list[2]

        source = 'SuperJob'
        link = response.url
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, currency=currency, source=source, link=link)

    def cut_the_sal(self, sal_list):
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
