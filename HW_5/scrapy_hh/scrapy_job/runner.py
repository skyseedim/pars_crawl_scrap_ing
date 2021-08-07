from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from HWs.HW_5.scrapy_hh.scrapy_job import settings
from HWs.HW_5.scrapy_hh.scrapy_job.spiders.hhru import HhruSpider
from HWs.HW_5.scrapy_hh.scrapy_job.spiders.sjru import SJSpider


if __name__ == '__main__':
	crawler_settings = Settings()
	crawler_settings.setmodule(settings)
	process = CrawlerProcess(settings=crawler_settings)
	process.crawl(HhruSpider)
	process.crawl(SJSpider)
	process.start()
