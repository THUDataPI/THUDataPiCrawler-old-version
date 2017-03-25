# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    pay = scrapy.Field()
    publish_time = scrapy.Field()
    requirement = scrapy.Field()
    responsibility = scrapy.Field()
    department = scrapy.Field()
    report_to = scrapy.Field()
    required_major = scrapy.Field()
    subordinates_num = scrapy.Field()

    company_name = scrapy.Field()
    company_size = scrapy.Field()
    company_address = scrapy.Field()
    company_type = scrapy.Field()
    company_industry = scrapy.Field()
    company_finance = scrapy.Field()
