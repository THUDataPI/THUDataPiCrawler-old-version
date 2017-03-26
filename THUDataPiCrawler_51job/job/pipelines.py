# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import scrapy
import sqlite3


class JobPipeline(object):
    def __init__(self):
        # 初始化数据库
        self.connection = sqlite3.connect('./sqlite.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS qcwy ' \
                    '(id INTEGER PRIMARY KEY,' \
                    'url VARCHAR,' \
                    'company_name VARCHAR,'
                    'job_position VARCHAR,'
                    'city VARCHAR,'
                    'salary VARCHAR,'
                    'company_type VARCHAR,'
                    'company_size VARCHAR,'
                    'company_area VARCHAR,'
                    'experience_requirement VARCHAR,'
                    'education_requirement VARCHAR,'
                    'recruiting_number VARCHAR,'
                    'posted_date VARCHAR,'
                    'job_tag VARCHAR,'
                    'job_info TEXT,'
                    'company_info TEXT'
                    ')')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS lagou ' \
                    '(id INTEGER PRIMARY KEY,' \
                    'url VARCHAR,' \
                    'company_name VARCHAR'
                    ')')
        self.count = 0

    def process_item(self, item, spider):
        if spider.name == 'qcwy':
            self.cursor.execute("select * from qcwy where url=?", (item['url'],))
            result = self.cursor.fetchone()
            if result:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.cursor.execute(
                    """INSERT INTO qcwy 
                    (url, job_position, company_name, city, salary, company_type,
                    company_size, company_area, experience_requirement,
                    education_requirement, recruiting_number, posted_date,
                    job_tag, job_info, company_info) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", 
                       (item['url'], 
                        item['job_position'],
                        item['company_name'],
                        item['city'],
                        item['salary'],
                        item['company_type'],
                        item['company_size'],
                        item['company_area'],
                        item['experience_requirement'],
                        item['education_requirement'],
                        item['recruiting_number'],
                        item['posted_date'],
                        item['job_tag'],
                        item['job_info'],
                        item['company_info'],))
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
