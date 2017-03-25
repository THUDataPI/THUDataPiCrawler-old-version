# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()  # 招聘信息链接
    # 职位基本信息
    job_position = scrapy.Field(default='')  # 职位
    city = scrapy.Field(default='')  # 所属城市
    salary = scrapy.Field(default='')  # 工资

    # 公司基本信息
    company_name = scrapy.Field(default='')  # 公司名称
    company_url = scrapy.Field(default='')  # 公司链接
    company_type = scrapy.Field(default='')  # 公司性质
    company_size = scrapy.Field(default='')  # 公司规模
    company_area = scrapy.Field(default='')  # 公司领域
    # department_name = scrapy.Field()  # 部门名称


    experience_requirement = scrapy.Field(default='')  # 经验要求
    education_requirement = scrapy.Field(default='')  # 学历要求 
    recruiting_number = scrapy.Field(default='')  # 招聘人数
    posted_date = scrapy.Field(default='')  # 发布日期
    job_tag = scrapy.Field(default='')  # 福利等

    job_info = scrapy.Field()  # 职位信息
    job_location = scrapy.Field(default='')  # 工作地址
    company_info = scrapy.Field(default='')  # 公司信息


class QCWYItem(JobItem):
    """前程无忧"""
    pass


class LagouItem(JobItem):
    """拉勾网"""
    pass    
        

class ZhipinItem(JobItem):
    """Boss直聘"""
    pass


class ZLZPItem(JobItem):
    """智联招聘"""
    pass