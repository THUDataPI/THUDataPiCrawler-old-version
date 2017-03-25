# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from liepin.items import LiepinItem
from urlparse import urljoin
from utils import is_match
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
                div_right_blcok_post = sel.xpath('//div[@class="right_blcok_post"]')

                item['url'] = current_url
                item['name'] = div_about_position.xpath('//h1/text()').extract()[0]  # [0]
                item['pay'] = div_about_position.xpath('//p[@class="job-item-title"]/text()').extract()[0].strip()  # [0]
                item['publish_time'] = div_about_position.xpath('//p[@class="basic-infor"]/span[2]/text()').extract()[-1].strip()  # [-1]
                item['requirement'] = div_about_position.xpath('//div[@class="job-qualifications"]/span/text()').extract()[0]
                item['responsibility'] = div_about_position.xpath(u'//h3[text()="职位描述："]/following::div[1]/text()').extract()
                item['responsibility'] = ''.join(item['responsibility'])

                ul_other_info_text = div_about_position.xpath(u'//h3[text()="其他信息："]/following::div[1]/ul/li/label/text()').extract()
                item['department'] = ul_other_info_text[0]
                item['required_major'] = ul_other_info_text[1]
                item['report_to'] = ul_other_info_text[2]
                item['subordinates_num'] = ul_other_info_text[3]

                item['company_name'] = div_about_position.xpath('//h3/a/text()').extract()[0]  # [0]
                company_industry = sel.xpath('//div[@class="company-infor"]/ul/li/a/text()').extract()
                if company_industry is None or len(company_industry) is 0:
                    item['company_industry'] = sel.xpath('//div[@class="company-infor"]/ul/li/text()').extract()[0].strip()
                else:
                    item['company_industry'] = company_industry[0].strip()

                ul_company_detail_text = sel.xpath('//div[@class="company-infor"]/ul/li/text()').extract()
                # print ul_company_detail_text
                item['company_type'] = ul_company_detail_text[-1].strip()
                for li_text in ul_company_detail_text:
                    if u'人' in li_text:
                        item['company_size'] = li_text.strip()
                    elif u'轮' in li_text:
                        item['company_finance'] = li_text.strip()
                item['company_address'] = sel.xpath('//div[@class="company-infor"]/p/text()').extract()[-1]

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
