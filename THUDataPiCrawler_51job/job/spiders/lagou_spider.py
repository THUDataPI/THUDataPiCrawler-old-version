import scrapy
from job.items import JobItem
import re



class LagouSpider(scrapy.Spider):
    name = "lagou"

    def start_requests(self):
        # search_fields = [r'大数据', r'数据分析', r'数据运营', r'数据挖掘']
        search_fields = ['大数据',]
        urls = [
            'https://www.lagou.com/jobs/list_%s?labelWords=&fromSearch=true&suginput=' % field for field in search_fields
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})
            # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        job_urls = response.xpath('//p[@class="t1 "]//a/@href').extract()
        for job_url in job_urls:
            yield scrapy.Request(url=job_url, callback=self.parse_job_info)
        
        next_page_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})
            # yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job_info(self, response):
        pass