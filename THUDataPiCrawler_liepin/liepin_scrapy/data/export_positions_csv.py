# -*- coding: utf-8 -*-

import pymongo
import sys
import csv

reload(sys)
sys.setdefaultencoding("utf-8")

mc = pymongo.MongoClient()

field_names= ('hire_website','company_name','job_name','job_category','department',
                                  'location','job_nature','experience','education','salary','major',
                                  'hire_num','temptation','description','industry','company_nature',
                                  'finance','staff_num','company_website','publish_date','publish_website',
                                  'original_url')

f = open('positions.csv', 'wb')
csv_f = csv.DictWriter(f, fieldnames=field_names)
csv_f.writeheader()

col = mc.get_database('liepin').get_collection('positions')
cursor = col.find()
for pos in cursor:
    if 'staff_num' not in pos.keys():
        pos['staff_num'] = 'NULL'
    if 'hire_website' not in pos.keys():
        pos['hire_website'] = 'NULL'

    del pos['_id']
    for key in pos.keys():
        pos[key] = pos[key].replace('\n', ' ').replace(',', ' ').replace('，', ' ').strip()

    csv_f.writerow(pos)

