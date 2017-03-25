# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import re
import time


class ThudatapicrawlerPipeline(object):
    def process_item(self, item, spider):
        re_text = re.compile(r'>(.*?)<')     # 正则表达式提取文本
        #  ----------------提取工作标签-----------------
        job_highlights_list = re_text.findall(item['Job_Highlights'])
        while "" in job_highlights_list:        # 去除空字符串
            job_highlights_list.remove("")
        #  -----------------提取职位描述和职位要求------------
        job_description_list = re_text.findall(item['Job_Description_and_Job_Requirements'])
        while "" in job_description_list:        # 去除空字符串
            job_description_list.remove("")
        job_description_list.insert(0, '岗位职责')
        # --------------------提取行业标签----------------
        company_label = re_text.findall(item['Company_Label'])
        # company_label.remove("")
        # print(item['Company_Label'])
        # print(company_label[0])
        # ----------------------提取日期-----------------
        re_date1 = re.compile(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')     # 正则表达式提取日期
        re_date2 = re.compile(r'[0-9]-[0-9][0-9]')
        re_date3 = re.compile(r'[0-9][0-9]-[0-9][0-9]')
        re_date4 = re.compile(r'[0-9]-[0-9]')
        re_date5 = re.compile(r'[0-9][0-9]-[0-9]')
        date1 = re_date1.findall(item['Release_Time'])
        date2 = re_date2.findall(item['Release_Time'])
        date3 = re_date3.findall(item['Release_Time'])
        date4 = re_date4.findall(item['Release_Time'])
        date5 = re_date5.findall(item['Release_Time'])
        if date1:
            date = '{}-{}-{}'.format(date1[0][0:4], date1[0][5:7], date1[0][8:10])
        elif date2:
            date = '{}-{}-{}'.format(time.localtime().tm_year, date2[0][0:1], date2[0][2:4])
        elif date3:
            date = '{}-{}-{}'.format(time.localtime().tm_year, date3[0][0:2], date3[0][3:5])
        elif date4:
            date = '{}-{}-{}'.format(time.localtime().tm_year, date4[0][0:1], date4[0][2:3])
        elif date5:
            date = '{}-{}-{}'.format(time.localtime().tm_year, date5[0][0:2], date5[0][3:4])
        elif item['Release_Time'] == '今天更新':
            date = '{}-{}-{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
        elif item['Release_Time'] == '昨天更新':
            date = '{}-{}-{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday - 1)
        else:
            date = 'error'
        # print(date)
        # ----------------结果写入CSV文件----------------------
        with open('Job_information_chinahr.csv', 'a') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow([item['Company_Name'],
                             item['Job_Title'],
                             item['Job_Labels'],
                             item['Department_Name'],
                             item['Company_Profile'],
                             item['Company_Label'],
                             item['Company_Type'],
                             item['Financing_Stage'],
                             item['Company_Size'],
                             item['Company_Home_Page'],
                             item['Work_Place'],
                             item['Salary'],
                             job_highlights_list,
                             item['Job_Type'],
                             item['Experience'],
                             item['Education'],
                             job_description_list,
                             date,
                             item['Source_Site']
                             ])
