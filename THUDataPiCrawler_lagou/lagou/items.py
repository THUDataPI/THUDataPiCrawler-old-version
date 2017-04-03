# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field
class LagouItem(Item):
    url = Field()
    companyName = Field()
    positionName = Field()#职位名称
    industryField  = Field()#领域
    jobType = Field()#工作类型
    financeStage = Field()#公司发展阶段
    companySize = Field()#公司规模
    positionAdvantage = Field()#待遇
    city = Field()#工作地点
    position_describe = Field()#职位描述
    salary = Field()#薪资
    positionLabel  = Field()
    experience  = Field()
    degree  = Field()
    professionalRequirement  = Field()
    recruitNum  = Field()
    companyType  = Field()
    companyPage  = Field()
    releaseDate  = Field()
    releaseSite  = Field()
    department  = Field()



