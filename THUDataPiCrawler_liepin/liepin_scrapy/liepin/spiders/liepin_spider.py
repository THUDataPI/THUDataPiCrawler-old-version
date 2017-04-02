# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from liepin.items import LiepinItem
from urlparse import urljoin
from utils import *
from config import *
import logging

class LiepinSpider(Spider):
    name = "liepin"
    allowed_domains = CONFIG['allowed_domains']
    start_urls = CONFIG['start_urls']

    def parse(self, response):
        sel = Selector(response)
        current_url = response.url
        # print response.body
        # 详情页分析
        for detail_link in CONFIG['detail_link_rule']:

            if is_match(current_url, detail_link):
                print 'match detail_link page!', current_url
                item = LiepinItem()
                # items接收list，防止出现index out of range

                div_about_position = sel.xpath('//div[@class="about-position"]')
                # div_right_blcok_post = sel.xpath('//div[@class="right_blcok_post"]')

                item[u'hire_website'] = 'NULL'
                item[u'company_name'] = div_about_position.xpath('//h3/a/text()').extract()[0]  # [0]
                item[u'job_name'] = div_about_position.xpath('//h1/text()').extract()[0]  # [0]

                # judge if key terms in the job_name
                flag = False
                for term in data_related_terms:
                    if term in item[u'job_name']:
                        flag = True
                if flag is False:
                    return


                company_industry = sel.xpath('//div[@class="company-infor"]/ul/li/a/text()').extract()
                if company_industry is None or len(company_industry) is 0:
                    item[u'job_category'] = sel.xpath('//div[@class="company-infor"]/ul/li/text()').extract()[0].strip()
                else:
                    item[u'job_category'] = company_industry[0].strip()

                ul_other_info_text = div_about_position.xpath(u'//h3[text()="其他信息："]/following::div[1]/ul/li/label/text()').extract()
                item[u'department'] = ul_other_info_text[0]
                item[u'location'] = div_about_position.xpath('//p[@class="basic-infor"]/span[1]/a/text()').extract()[-1].strip()  # [-1]
                item[u'job_nature'] = u'全职'

                requirement = div_about_position.xpath('//div[@class="job-qualifications"]/span/text()').extract()
                item[u'experience'] = requirement[1]
                item[u'education'] = requirement[0]

                item[u'salary'] = div_about_position.xpath('//p[@class="job-item-title"]/text()').extract()[0].strip()  # [0]
                item[u'salary'] = process_salary(item[u'salary'])

                item[u'major'] = ul_other_info_text[1]

                item[u'hire_num'] = 'NULL'

                description = div_about_position.xpath(u'//h3[text()="职位描述："]/following::div[1]/text()').extract()

                item[u'temptation'] = div_about_position.xpath(u'//div[@class="tag-list"]/span[@class="tag"]/text()').extract()
                item[u'temptation'] = ','.join(item[u'temptation'])

                item[u'description'] = "\n".join(description)

                ul_company_detail_text = sel.xpath('//div[@class="company-infor"]/ul/li/text()').extract()
                # print ul_company_detail_text
                item[u'industry'] = sel.xpath('//div[@class="company-infor"]/ul/li[1]/a/text()').extract()[0]
                item[u'company_nature'] = ul_company_detail_text[-1].strip()
                item[u'finance'] = 'NULL'
                for li_text in ul_company_detail_text:
                    if u'人' in li_text:
                        item[u'staff_num'] = li_text.strip()
                    elif u'轮' in li_text:
                        item[u'finance'] = li_text.strip()

                item[u'company_website'] = 'NULL'
                item[u'publish_date'] = div_about_position.xpath('//p[@class="basic-infor"]/span[2]/text()').extract()[-1].strip()  # [-1]
                item[u'publish_date'] = get_publish_time(item[u'publish_date'])
                item[u'publish_website'] = 'NULL'
                item[u'original_url'] = current_url

                # item['requirement'] = div_about_position.xpath('//div[@class="job-qualifications"]/span/text()').extract()[0]
                # item['report_to'] = ul_other_info_text[2] 汇报对象
                # item['subordinates_num'] = ul_other_info_text[3] 下属人数
                # company_website = div_about_position.xpath('//h3/a/@href').extract()
                # item['company_website'] = 'NULL' if len(company_website) == 0 else company_website[0]
                # item['company_address'] = sel.xpath('//div[@class="company-infor"]/p/text()').extract()[-1]

                print item.__dict__
                yield item

        # 过滤出所有的列表页和详情页进行回调。
        for url in sel.xpath('//a/@href').extract():
            url = urljoin(current_url, url)
            # print url
            for list_link in CONFIG['list_link_rule']:
                if is_match(url, list_link):
                    # print 'match list_link page! ', url
                    # log.msg('list_url: %s' % url, level=log.INFO)
                    yield Request(url, callback=self.parse)

            for detail_link in CONFIG['detail_link_rule']:
                if is_match(url, detail_link):
                    print 'match detail_link page!', url
                    # log.msg('detail_url: %s' % url, level=log.INFO)
                    yield Request(url, callback=self.parse)
