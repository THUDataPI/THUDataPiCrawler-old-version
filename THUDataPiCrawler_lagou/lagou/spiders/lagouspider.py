# -*- coding: utf-8 -*-
import sys
from scrapy.selector import Selector
from selenium import webdriver
import time
import datetime
from scrapy.spiders import  Spider
from scrapy.http import Request
from ..items import LagouItem

reload(sys)
sys.setdefaultencoding("utf-8")

class LagouSpider( Spider):
    name = "lagouspider"
    allowed_domains = ["www.lagou.com"]
    start_urls = ["https://www.lagou.com/" ]
    #set the terminal query parameters
    #def __init__(self,query):
    #    self.query = query
    #rewrite the request method
    def start_requests(self):
        search_fields = [u'']
        #search_fields = self.query
        root_url = 'https://www.lagou.com'
        urls = []
        for field in search_fields:
            driver = webdriver.Ie('C:\Program Files\Internet Explorer\IEDriverServer.exe')  # open browser
            driver.get(root_url)  # open root url
            time.sleep(1)  # waiting for closing dialog
            driver.find_element_by_id('search_input').send_keys('%s' % field)
            driver.find_element_by_id('search_button').click()
            time.sleep(2)  # waiting for redirection
            i = 0
            flag = True#if there is no page column,then skip the search 
            try:
                class_name = driver.find_element_by_xpath('//span[@action="next"]').get_attribute('class')
                print class_name
            except Exception:
                 flag = False
                 print "position is too sparse!"
            ##### to crawl 16 pages#####
            while  flag and class_name == "pager_next " and i < 16:#there is a space after pager_next~
                time.sleep(1) 
                position_links = driver.find_elements_by_class_name('position_link')
                for position_link in position_links:
                    job_url = position_link.get_attribute('href')
                    print('adding new seed url: %s' % job_url)
                    urls.append(job_url)
                for url in urls:
                    yield  Request(url=url, callback=self.parse_page)
                i += 1
                print "parsing page: ",i
                driver.close()
                driver.find_element_by_class_name('pager_next ').click()#go to the next page
                class_name = driver.find_element_by_xpath('//span[@action="next"]').get_attribute('class')
    def parse_page(self, response):
        job = Selector(response)
        item = LagouItem()
        item['url'] = response.url
        item['companyName'] = job.xpath('//div[@class="company"]/text()').extract()
        item['positionName']= job.xpath('//div[@class="ceil"]/div[@class="ceil-content"]/span[@class="ceil-job"]/text()').extract()
        industryField = job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[1]/text()').extract()[1]
        item['industryField'] = "NULL" if industryField == [] else industryField 
        financeStage = job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[2]/text()').extract()[1]
        item['financeStage'] = "NULL" if financeStage == [] else financeStage
        side_result = response.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li').extract()
        # to address the proplem of unknown size of terms
        if  len(side_result)==4:
            item['companySize']= job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[3]/text()').extract()[1]
            item['companyPage'] = job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[4]/a/text()').extract()
        elif len(side_result) == 5:
            item['companySize']= job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[4]/text()').extract()[1]
            item['companyPage'] = job.xpath('//div[@class="content_r"]/dl[@id="job_company"]/dd/ul[@class="c_feature"]/li[5]/a/text()').extract()
        else:
            item['companySize'] = "NULL"
            item['companyPage'] = "NULL"
        item['positionAdvantage'] = job.xpath('//div[@id="container"]/div[@class="content_l fl"]/dl/dd[@class="job-advantage"]/p/text()').extract()
        item['salary']= job.xpath('//div[@class="ceil"]/div[@class="ceil-content"]/span[@class="ceil-salary"]/text()').extract()
        position_head = job.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        try:
            item['city'] = position_head[1]
            item['jobType'] = position_head[4]
            item['degree'] = position_head[3]
            item['experience'] = position_head[2]
        except Exception:
            item['city'] = "NULL"
            item['jobType'] = "NULL"
            item['degree'] ="NULL"
            item['experience'] = "NULL"
        item['professionalRequirement'] = job.xpath('//div[@id="container"]/div[@class="content_l fl"]/dl/dd[@class="job_bt"]/div/p/text()').extract()
        
        item['position_describe'] = job.xpath('//div[@id="container"]/div[@class="content_l fl"]/dl/dd[@class="job_bt"]/div/p/text()').extract()
        item['releaseDate'] =  ''.join(job.xpath('//p[@class="publish_time"]/text()').extract()).split()[0]
        # to unify release time
        if len(item['releaseDate'])==3:
            daypre = int(item['releaseDate'][0])
            item['releaseDate'] =  (datetime.datetime.now()+datetime.timedelta(days=-daypre)).strftime('%Y-%m-%d')
        elif len(item['releaseDate'])==5:
            item['releaseDate'] = datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            item['releaseDate'] = item['releaseDate']
        item['department'] = job.xpath('//div[@class="company"]/text()').extract()
        item['companyType'] =  "NULL"
        item['recruitNum'] = "NULL"
        item['positionLabel'] = job.xpath('//li[@class="labels"]/text()').extract()
        item['releaseSite'] = u"拉勾网"
        print item
        return item






