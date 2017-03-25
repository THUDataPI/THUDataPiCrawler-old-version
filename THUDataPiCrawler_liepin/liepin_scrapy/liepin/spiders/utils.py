# -*- coding:utf-8 -*-
'''
    可以写一些公共方法
'''

import re
import datetime


# 正则匹配链接规则，符合规则的返回True
def is_match(url, rule):
    obj = re.compile(rule).match(url)
    if obj is None:
        return False
    else:
        return True

# 发布日期转换，统一转换成datatime格式
def get_publish_time(pub):
    today = datetime.date.today()
    if pub.find("小时") != -1 or pub.find("分钟") != -1 or pub.find("刚刚") != -1:
        publish_time = today
    elif pub.find("昨天") != -1:
        publish_time = today - datetime.timedelta(days=1)
    elif pub.find("前天") != -1:
        publish_time = today - datetime.timedelta(days=2)
    else:
        result = re.search('\d+-\d+-\d+', pub)
        if result:
            publish_time = datetime.datetime.strptime(result.group(), "%Y-%m-%d").date()
        else:
            publish_time = None
    return publish_time