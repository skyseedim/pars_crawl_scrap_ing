# Define here the models for your scraped items
import scrapy


class JobparserItem(scrapy.Item):
   # define the fields for your item here like:
   # name = scrapy.Field()
   _id = scrapy.Field()
   name = scrapy.Field()
   salary_min = scrapy.Field()
   salary_max = scrapy.Field()
   currency = scrapy.Field()
   source = scrapy.Field()
   link = scrapy.Field()
   pass
