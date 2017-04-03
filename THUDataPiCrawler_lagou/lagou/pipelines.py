# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
file = xlwt.Workbook()
writeSheet = file.add_sheet("joblist", cell_overwrite_ok=True)
count = 0
class LagouPipeline(object):
    def process_item(self,item, spider):
        print item
        global count
        print "---pipeline processing item ---"
        writeSheet.write(count, 0, item['positionName'])#职位名字
        writeSheet.write(count, 1, item['positionLabel'])#分类标签
        writeSheet.write(count, 2, item['department'])#部门
        writeSheet.write(count, 3, item['city'])#工作地点
        writeSheet.write(count, 4, item['jobType'])#工作性质（全职实习）
        writeSheet.write(count, 5, item['experience'])#经验
        writeSheet.write(count, 6, item['degree'])#学历
        writeSheet.write(count, 7, item['salary'])#薪资
        writeSheet.write(count, 8, item['professionalRequirement']) #专业要求
        writeSheet.write(count, 9, item['recruitNum']) #招聘人数
        writeSheet.write(count, 10, item['positionAdvantage']) # 职位诱惑
        writeSheet.write(count, 11, item['position_describe'])  #岗位介绍
        writeSheet.write(count, 12, item['companyName'])#公司名称
        writeSheet.write(count, 13, item['industryField'])#行业
        writeSheet.write(count, 14, item['companyType'])#公司性质
        writeSheet.write(count, 15, item['financeStage'])#融资阶段
        writeSheet.write(count, 16, item['companySize'])#规模
        writeSheet.write(count, 17, item['companyPage'])#主页
        writeSheet.write(count, 18, item['releaseDate'])#发布日期
        writeSheet.write(count, 19, item['releaseSite'])#发布网站
        writeSheet.write(count, 20, item['url'])#原始URL
        file.save('THUDataPiCrawler_chinahr_2017_04_02.xlsTHUDataPiCrawler_lagou_2017_04_02.xls')
        count += 1
        print  'write into excel successfully!'
