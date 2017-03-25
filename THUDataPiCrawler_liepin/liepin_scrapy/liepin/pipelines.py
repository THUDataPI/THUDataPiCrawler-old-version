# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import hashlib
import traceback
import pymongo
from spiders.utils import *

mongo_client = pymongo.MongoClient()


# 每一个招聘信息都会计算出一个md5，作为mysql数据库的UNIQUE KEY，避免重复写入数据
def md5str(strr):
    m = hashlib.md5(strr)
    md5 = m.hexdigest().lower()
    return md5


# 将职位需求拼接到一起，方便写入数据库
def get_require(requires):
    require = ''
    for r in requires:
        require += r + ' '
    return require.strip().encode('utf-8')


class MongoPipeline(object):

    def get_cup(self, item):
        url = item['url']
        name = item['name'][0].strip().encode('utf-8')
        company_name = item['company_name'][0].strip().encode('utf-8')
        if item['company_size']:
            company_size = item['company_size'][4].strip().encode('utf-8')
            company_address = item['company_address'][-1].strip().encode('utf-8')
            company_type = item['company_type'][-3].strip().encode('utf-8')
        else:
            company_size = None
            company_address = None
            company_type = None
        pay = item['pay'][0].strip().encode('utf-8')
        publish_time = get_publish_time(item['publish_time'][-1].encode('utf-8'))
        require = get_require(item['requires'])
        code_md5 = md5str(url + name + company_name + require)

        position_dict = dict()
        position_dict['url'] = url
        position_dict['name'] = name
        position_dict['company_name'] = company_name
        position_dict['publish_time'] = publish_time
        position_dict['require'] = require
        position_dict['pay'] = pay
        position_dict['company_size'] = company_size
        position_dict['company_address'] = company_address
        position_dict['company_type'] = company_type
        position_dict['code_md5'] = code_md5
        return position_dict

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client.get_database('liepin')

    def close_spider(self, spider):
        self.client.close()

    # 捕捉错误信息写入log
    def process_item(self, item, spider):
        try:
            # position_dict = self.get_cup(item)
            self.db['positions'].insert(dict(item))
            print 'data inserted!'
        except Exception, e:
            print 'url is: %s, error is: %s.' % (item['url'], traceback.format_exc()),
            print e
            traceback.print_exc()
        finally:
            return item
