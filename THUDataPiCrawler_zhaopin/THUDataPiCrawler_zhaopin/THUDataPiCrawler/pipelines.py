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
        # if item['Job_Highlights'] is not None:
        job_highlights_list = re_text.findall(item['Job_Highlights'])
        while "" in job_highlights_list:  # 去除空字符串
            job_highlights_list.remove("")
        job_highlights = ''
        for i in range(len(job_highlights_list)):
            job_highlights = job_highlights + job_highlights_list[i] + ','
        if len(job_highlights) == 0:
            job_highlights = 'NULL'
        #  -----------------提取职位描述和职位要求------------
        job_description_list = re_text.findall(item['Job_Description_and_Job_Requirements'])
        while "" in job_description_list:        # 去除空字符串
            job_description_list.remove("")
        job_description = '岗位职责:'
        for i in range(len(job_description_list)):
            if ('工作地址：' in job_description_list[i]) or ('联系方式：' in job_description_list[i]):
                break
            elif '岗位职责' in job_description_list[i]:
                continue
            else:
                job_description = job_description + job_description_list[i].replace(' ', '')
        job_description = job_description + ' '
        # print(job_description)
        # --------------------工作地点处理-----------------
        # print(item['Work_Place'])
        if '区' in item['Work_Place']:
            work_place = item['Work_Place'].replace(' ', '-')
        else:
            work_place = item['Work_Place'] + '-NULL'
        # --------------------经验-------------------------
        if '年以下' in item['Experience']:
            experience = item['Experience'].replace('以下', '经验')
        elif '年以上' in item['Experience']:
            experience = item['Experience']
        elif '年' in item['Experience']:
            experience = item['Experience'] + '经验'
        elif '应届' in item['Experience']:
            experience = '0年经验'
        else:
            experience = item['Experience']
        # -----------------招聘人数----------------------
        if '若干' in item['Number']:
            number = '-1'
        elif '不限' in item['Number']:
            number = '-2'
        else:
            number = item['Number']
        # ----------------结果写入CSV文件----------------------
        with open('THUDataPiCrawler_zhaopin_2017_04_04.csv', 'a') as f:
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
                             number,                     # 招聘人数
                             job_highlights,             # 职位诱惑
                             job_description,            # 职位介绍
                             item['Company_Name'],
                             item['Company_Label'],
                             item['Company_Type'],
                             item['Financing_Stage'],
                             item['Company_Size'],
                             item['Company_Home_Page'],
                             item['Release_Time'],
                             item['Source_Site'],
                             item['Source_URL']
                             ])
