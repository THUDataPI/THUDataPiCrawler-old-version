# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import scrapy
from scrapy.exceptions import DropItem
import sqlite3


class JobPipeline(object):
    def __init__(self):
        # 初始化数据库
        self.connection = sqlite3.connect('./sqlite.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS qcwy '
                    '(id INTEGER PRIMARY KEY,'
                    'position VARCHAR,'
                    'position_tag VARCHAR,'
                    'department VARCHAR,'
                    'city VARCHAR,'
                    'position_type VARCHAR,'
                    'experience_requirement VARCHAR,'
                    'education_requirement VARCHAR,'
                    'salary VARCHAR,'
                    'major_requirement VARCHAR,'
                    'recruiting_number VARCHAR,'
                    'position_advantage VARCHAR,'
                    'position_info TEXT,'
                    'company VARCHAR,'
                    'company_industry VARCHAR,'
                    'company_type VARCHAR,'
                    'company_finance VARCHAR,'
                    'company_size VARCHAR,'
                    'company_url VARCHAR,'
                    'posted_date VARCHAR,'
                    'posted_website VARCHAR,'
                    'posted_url VARCHAR'
                    ')')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS lagou '
                    '(id INTEGER PRIMARY KEY,'
                    'url VARCHAR,'
                    'company_name VARCHAR'
                    ')')
        self.count = 0

    def process_item(self, item, spider):
        if spider.name == 'qcwy':
            self.cursor.execute("select * from qcwy where posted_url=?", (item['posted_url'],))
            result = self.cursor.fetchone()
            if result:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.cursor.execute(
                    """INSERT INTO qcwy 
                    (position, position_tag, department, city, position_type, 
                    experience_requirement, education_requirement, salary,
                    major_requirement, recruiting_number, position_advantage,
                    position_info, company, company_industry, company_type,
                    company_finance, company_size, company_url, posted_date,
                    posted_website, posted_url) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", 
                       (item['position'], 
                        item['position_tag'], 
                        item['department'], 
                        item['city'], 
                        item['position_type'], 
                        item['experience_requirement'], 
                        item['education_requirement'], 
                        item['salary'], 
                        item['major_requirement'], 
                        item['recruiting_number'], 
                        item['position_advantage'], 
                        item['position_info'], 
                        item['company'], 
                        item['company_industry'], 
                        item['company_type'], 
                        item['company_finance'], 
                        item['company_size'], 
                        item['company_url'], 
                        item['posted_date'], 
                        item['posted_website'], 
                        item['posted_url']))
                self.connection.commit()
        elif spider.name == 'lagou':
            self.cursor.execute("select * from lagou where url=?", (item['url'],))
            result = self.cursor.fetchone()
            if result:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.cursor.execute(
                    """INSERT INTO lagou 
                    (url, company_name) 
                       VALUES (?,?);""", 
                       (item['url'], 
                        item['company_name']))
                self.connection.commit()
        self.count += 1
        print('%d job info pages parsed' % self.count)
        return item
