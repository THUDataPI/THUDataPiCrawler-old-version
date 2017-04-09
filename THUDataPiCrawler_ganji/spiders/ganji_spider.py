# -*- coding: utf-8 -*-

import scrapy
from THUDataPiCrawler_ganji.items import JobItem
import re
import time


class ScrapySpiderSpider(scrapy.Spider):
    name = "ganji"
    allowed_domains = ["bj.ganji.com","sh.ganji.com","gz.ganji.com",'wh.ganji.com',
			'sz.ganji.com', 'wh.ganji.com', 'nj.ganji.com', 'tj.ganji.com', 'hz.ganji.com', 'cd.ganji.com', 'cq.ganji.com', 'cs.ganji.com', 'cc.ganji.com', 'dl.ganji.com', 'dg.ganji.com', 'fz.ganji.com', 'foshan.ganji.com', 'gy.ganji.com', 'gl.ganji.com', 'huizhou.ganji.com', 'hrb.ganji.com', 'hf.ganji.com', 'nmg.ganji.com', 'hn.ganji.com', 'jn.ganji.com', 'km.ganji.com', 'lz.ganji.com', 'xz.ganji.com', 'nb.ganji.com', 'nn.ganji.com', 'nc.ganji.com', 'qd.ganji.com', 'sy.ganji.com', 'sjz.ganji.com', 'su.ganji.com']

    def start_requests(self):
        search_fields = ['大数据', '数据分析', '数据运营', '数据挖掘', '爬虫',
                         '抓取', '可视化', 'hadoop', 'spark', 'hbase', 'hive']
       # search_fields = ['数据开发', '数据工程', '数据处理', '数据科学家', '数据工程师',
        #                 '数据架构师', '数据采集', '数据建模', '数据平台', '数据研发', '数据管理', '数据挖据', '数据统计', '数据产品', '数据方向', '数据仓库',
         #                '数据研究', '数据算法', '数据蜘蛛', '金融数据', '数据专员', '数据主管', '数据项目经理', '数据整合', '数据模型', '数据支撑', '财务数据',
          #               '数据专家', '数据报送', '数据挖据', '数据中心', '数据移动', '数据标准''数据风']
        #search_fields = ['大数据']
        urls = [
            #'http://bj.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields
            #['http://sz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields]
            #['http://wh.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields]
            ['http://nj.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://tj.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://hz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://sh.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://gz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://sz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://wh.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://nj.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://tj.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://hz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://cd.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://cq.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://cs.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://cc.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://dl.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://dg.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://fz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://foshan.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://gy.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://gl.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://huizhou.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://hrb.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://hf.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://nmg.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://hn.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://jn.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://km.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://lz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://xz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://nb.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://nn.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://nc.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://qd.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://sy.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://sjz.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields],
            ['http://su.ganji.com/zhaopin/s/_%s/?from=zhaopin_indexpage' % field for field in search_fields]
        ]

        for urlList in urls:
            #yield scrapy.Request(url=urlList, callback=self.parse)
            for url in urlList:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        print("parse")
        job_urls = response.xpath('//div[@class="fl ml-5"]//div[@class="fl j-title"]/a/@href').extract()
        #job_urls=['http://sz.ganji.com/zpjisuanjiwangluo/1987353363x.htm']
        #job_urls=['http://bj.ganji.com/zpjisuanjiwangluo/2164903342x.htm']

        for job_url in job_urls:
            print(response.urljoin(job_url))
            yield scrapy.Request(response.urljoin(job_url), callback=self.parse_job_info)


        next_page_url = response.xpath('//a[contains(.,"下一页")]/@href').extract_first()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_job_info(self, response):
        print("parse_job_info")
        item = JobItem()
        print("parse job info from %s" % response.url)
        item['posted_url'] = str(response.url)
        item['posted_website'] = '赶集网'

        item['company'] = response.xpath('//span[@class="firm-name"]/a/text()').extract_first().strip()
        item['company_url'] = response.xpath('//span[@class="firm-name"]/a/@href').extract_first()
        posted_date = response.xpath('//span[contains(.,"更新时间")]/text()').extract_first().split(u'：')[1]
        if posted_date == '今天':
            d = time.strftime("%d/%m/%Y", time.localtime())
        else:
            d = time.strftime("%d/%m/%Y", time.strptime("2017-"+posted_date, "%Y-%m-%d"))

        item['posted_date'] = d
        item['position'] = response.xpath('//li[@class="fl" and contains(.,"职位名称：")]/em/a/text()').extract_first()
        item['salary'] = response.xpath('//li[@class="fl" and contains(.,"月")]/em/text()').extract_first()
        item['education_requirement'] = response.xpath('//li[@class="fl" and contains(.,"最低学历：")]/em/text()').extract_first()
        item['experience_requirement'] = response.xpath('//li[@class="fl" and contains(.,"工作经验：")]/em/text()').extract_first().strip()
        item['recruiting_number'] = response.xpath('//li[@class="fl" and contains(.,"招聘人数：")]/em/text()').extract_first()
        city = response.xpath('//li[@class="fl w-auto" and contains(.,"工作地点：")]/em/a/text()').extract()
        if len(city) == 1:
            item['city']=city[0]+'-NULL'
        else:
            item['city']='-'.join(city)
        advantage = response.xpath(u'//div[@class="d-welf-items"]/ul/li/text()').extract()
        item['position_advantage']=','.join(advantage)
        item['company_industry'] = response.xpath('//div[@class="rt_txt" and contains(.,"公司行业")]/span/a/text()').extract_first().replace('/',',')
        item['company_type'] = response.xpath('//div[@class="rt_txt" and contains(.,"公司性质：")]/span/a/text()').extract_first()
        item['company_size'] = response.xpath('//div[@class="rt_txt" and contains(.,"公司规模：")]/span/text()').extract_first()
        info = response.xpath('//div[@class="deta-Corp"]/text()').extract()
        item['position_info'] = "".join(info).strip()
        ptype = response.xpath('//span[@class="fc-999"]/text()').extract_first()
        item['position_type'] = re.findall(r"（(.+)）",ptype)[0]
        item['position_tag'] = "NULL"
        item['department'] = "NULL"
        item["major_requirement"] = "NULL"
        item['company_finance'] = "NULL"
        yield item

