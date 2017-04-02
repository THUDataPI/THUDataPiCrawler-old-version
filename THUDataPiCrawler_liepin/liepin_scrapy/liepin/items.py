# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    hire_website = scrapy.Field()
    company_name = scrapy.Field()
    job_name = scrapy.Field()
    job_category = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    job_nature = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    salary = scrapy.Field()
    major = scrapy.Field()
    hire_num = scrapy.Field()
    temptation = scrapy.Field()
    description = scrapy.Field()
    industry = scrapy.Field()
    company_nature = scrapy.Field()
    finance = scrapy.Field()
    staff_num = scrapy.Field()
    company_website = scrapy.Field()
    publish_date = scrapy.Field()
    publish_website = scrapy.Field()
    original_url = scrapy.Field()

