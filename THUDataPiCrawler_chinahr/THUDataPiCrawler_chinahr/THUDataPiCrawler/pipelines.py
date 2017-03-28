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
        if item['Job_Highlights'] is not None:
            job_highlights_list = re_text.findall(item['Job_Highlights'])
            while "" in job_highlights_list:        # 去除空字符串
                job_highlights_list.remove("")
            job_highlights = ''
            for i in range(len(job_highlights_list)):
                job_highlights = job_highlights + job_highlights_list[i] + ','
        else:
            job_highlights = 'NULL'
        # print(job_highlights)
        #  -----------------提取职位描述和职位要求------------
        job_description_list = re_text.findall(item['Job_Description_and_Job_Requirements'])
        if len(job_description_list) == 0:
            job_description = '岗位职责:' + item['Job_Description_and_Job_Requirements'][28:-6]
            job_description = job_description.replace(' ', '').replace('\n', '')
            # print(job_description_list)
            # print(job_description)
        else:
            while "" in job_description_list:        # 去除空字符串
                job_description_list.remove("")
            job_description = '岗位职责:'
            for i in range(len(job_description_list)):
                job_description = job_description + job_description_list[i].replace(' ', '')
            job_description = job_description + ' '
        # print(job_description)
        # --------------------工作地点处理-----------------
        if '区' in item['Work_Place']:
            work_place = item['Work_Place'].replace(' ', '-')
        else:
            work_place = item['Work_Place'] + '-NULL'
        # --------------------经验要求处理----------------
        if len(item['Experience']) == 0:
            experience = 'NULL'
        else:
            if '应届' in item['Experience']:
                experience = '0年经验'
            elif '以上' in item['Experience']:
                experience = item['Experience']
            else:
                experience = item['Experience'][2:]
                experience = experience + item['Experience'][0:2]
        # print(experience)
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
        with open('THUDataPiCrawler_chinahr_2017_03_27.csv', 'a') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow([item['Job_Title'],          # 职位名称
                             item['Job_Labels'],         # 职位分类标签
                             item['Department_Name'],    # 部门
                             work_place,                 # 工作地点
                             item['Job_Type'],           # 工作性质
                             experience,                 # 经验
                             item['Education'],          # 学历
                             item['Salary'],             # 薪资
                             item['Major'],              # 专业要求
                             item['Number'],             # 招聘人数
                             job_highlights,             # 职位诱惑
                             job_description,            # 职位介绍
                             item['Company_Name'],
                             item['Company_Label'],
                             item['Company_Type'],
                             item['Financing_Stage'],
                             item['Company_Size'],
                             item['Company_Home_Page'],
                             date,
                             item['Source_Site'],
                             item['Source_URL']
                             ])
