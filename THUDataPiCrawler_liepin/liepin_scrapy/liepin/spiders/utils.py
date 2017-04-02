# -*- coding:utf-8 -*-
'''
    可以写一些公共方法
'''

import re
import datetime


data_related_terms = [u'数据', u'人工智能', u'机器学习', u'深度学习', u'爬虫', u'抓取', u'可视化', u'Hadoop', u'hadoop',
                      u'Spark', u'spark', u'HBase', u'hbase', u'Hive', u'hive']

headers = {
    "Host": "www.liepin.com",
    'Cache-Control': 'max-age=0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://www.baidu.com",
    "Connection": "keep-alive"
}

# 正则匹配链接规则，符合规则的返回True
def is_match(url, rule):
    obj = re.compile(rule).match(url)
    if obj is None:
        return False
    else:
        return True


def process_salary(salary):
    if u'面议' in salary:
        return salary
    else:
        salary = salary.strip(u'万')
        splitted_salary = salary.split('-')
        splitted_salary = [int(x)*10000 for x in splitted_salary]
        processed_salary = '%d-%d' % (splitted_salary[0], splitted_salary[1])
        return processed_salary


# 发布日期转换，统一转换成datatime格式
def get_publish_time(pub):
    today = datetime.date.today()
    if pub.find(u"小时") != -1 or pub.find(u"分钟") != -1 or pub.find(u"刚刚") != -1:
        publish_time = today
    elif pub.find(u"昨天") != -1:
        publish_time = today - datetime.timedelta(days=1)
    elif pub.find(u"前天") != -1:
        publish_time = today - datetime.timedelta(days=2)
    else:
        result = re.search('\d+-\d+-\d+', pub)
        if result:
            publish_time = datetime.datetime.strptime(result.group(), "%Y-%m-%d").date()
        else:
            publish_time = None
    return str(publish_time)