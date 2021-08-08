import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.loader import ItemLoader
from ..items import LeroymerlinItem
from urllib.parse import urljoin
from scrapy.loader.processors import MapCompose


class LeroySpider(CrawlSpider):
    name = 'leroy'

    start_urls = ['https://leroymerlin.ru/catalogue/laminat/']
    custom_settings = {'DEPTH_LIMIT': 2}
    rules = (
        Rule(LinkExtractor(restrict_css='div.s1nb31eh_plp div.s1pmiv2e_plp a.bex6mjh_plp')),
        Rule(LinkExtractor(restrict_css='div.pedu908_plp div.phytpj4_plp div.c155f0re_plp a.bex6mjh_plp'), callback='parse_item')
    )

    def parse(self, response):
        first_link = ItemLoader(item=LeroymerlinItem(), response=response)
        first_link.add_xpath('file_name', '//h1/text()')
        first_link.add_xpath('file_urls', 'p//*[@id="picture-box-id-generated-5"]/img/@src',
                           MapCompose(lambda i: urljoin(response.url, i)))

        return first_link.load_item()


