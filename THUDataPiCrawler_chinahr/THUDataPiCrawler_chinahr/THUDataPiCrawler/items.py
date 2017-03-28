# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThudatapicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Company_Name = scrapy.Field()                          # 公司名称：如红茶移动
    Job_Title = scrapy.Field()                             # 职位名称：如数据分析工程师
    Job_Labels = scrapy.Field()                            # 职位类别标签：数据、数据挖掘
    Department_Name = scrapy.Field()                       # 职位所属部门名称：如技术部、商业服务部、市场部、产品部
    Company_Label = scrapy.Field()                         # 公司领域：如移动互联网、金融等
    Company_Type = scrapy.Field()                          # 公司性质：私企、外企、国企
    Financing_Stage = scrapy.Field()                       # 公司融资阶段：如不需要融资、上市公司、A 轮/B 轮/C 轮等
    Company_Size = scrapy.Field()                          # 公司规模：如 150-500 人
    Company_Home_Page = scrapy.Field()                     # 公司主页链接：如 http://redteamobile.com
    Work_Place = scrapy.Field()                            # 工作地点：如北京、深圳
    Salary = scrapy.Field()                                # 薪水：如 15k-20k
    Job_Highlights = scrapy.Field()                        # 职位诱惑：多金,技术大牛,核心技术人,非你莫属
    Job_Type = scrapy.Field()                              # 工作性质：全职、实习、兼职
    Experience = scrapy.Field()                            # 经历要求：例如经验1-3年
    Education = scrapy.Field()                             # 学历要求：例如本科及以上
    Job_Description_and_Job_Requirements = scrapy.Field()  # 职位描述：工作职责等具体说明 和 任职要求：技能资质等具体说明
    Release_Time = scrapy.Field()                          # 发布时间：如 2017-02-10（注意将“1 天前”这样的信息进行转换）
    Source_Site = scrapy.Field()                           # 网站名称：发布职位的招聘网站名称，如拉勾
    Source_URL = scrapy.Field()                            # 职位信息URL：抓取职位信息的URL
    Major = scrapy.Field()                                 # 专业要求：计算机
    Number = scrapy.Field()                                # 招聘人数：若干人
    # pass
