# -*- coding:utf-8 -*-
import logging

CONFIG = {
    'allowed_domains': ['www.liepin.com', 'liepin.com'],
    'start_urls': [u'https://www.liepin.com/zhaopin/?key=数据',
                   u'https://www.liepin.com/zhaopin/?key=爬虫',
                   u'https://www.liepin.com/zhaopin/?key=hadoop'],
    'detail_link_rule': ['https://www.liepin.com/job/[0-9]{9}\.shtml',
                         'https://www.liepin.com/a/[0-9]{7}\.shtml'],
    'list_link_rule': ['https://www.liepin.com/zhaopin/\?.*curPage=\d+']
}

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../liepin.log',
                filemode='w')