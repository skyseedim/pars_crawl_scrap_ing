# Scrapy settings for leroymerlin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'leroymerlin'

SPIDER_MODULES = ['leroymerlin.spiders']
NEWSPIDER_MODULE = 'leroymerlin.spiders'




DOWNLOAD_DELAY = 1



ITEM_PIPELINES = {'leroymerlin.pipelines.LeroymerlinPipeline': 100}
FILES_STORE = r'goods_images'

ROBOTSTXT_OBEY = True
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
