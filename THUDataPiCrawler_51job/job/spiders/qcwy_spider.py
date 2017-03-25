import scrapy
from job.items import JobItem
import re


def merge_string(str_list, pattern='[\t\r\n \xa0]', delimiter="\n"):
    if len(str_list) == 0:
        return ''
    for i in range(len(str_list)):
        if i == 0:
            s = str_list[0]
        else:
            s += (delimiter + str_list[i])
    s = re.sub(pattern, '', s)  # remove special characters
    return s


class QCWYSpider(scrapy.Spider):
    name = "qcwy"

    def start_requests(self):
        search_fields = [r'大数据', r'数据分析', r'数据运营', r'数据挖掘']
        # search_fields = ['大数据',]
        urls = [
            'http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword=%s&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % field for field in search_fields
        ]
        for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        job_urls = response.xpath('//p[@class="t1 "]//a/@href').extract()
        for job_url in job_urls:
            yield scrapy.Request(url=job_url, callback=self.parse_job_info)
        
        next_page_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            # yield scrapy.Request(next_page_url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_job_info(self, response):
        item = JobItem()
        print("parse job info from %s" % response.url)
        item['url'] = response.url 

        job_info = response.xpath('//div[@class="cn"]')
        item['company_name'] = job_info.xpath('p/a/text()').extract_first()
        item['job_position'] = job_info.xpath('h1/text()').extract_first()
        item['city'] = job_info.xpath('.//span[@class="lname"]/text()').extract_first()
        item['salary'] = job_info.xpath('./strong/text()').extract_first()

        company_str = job_info.xpath('./p[@class="msg ltype"]/text()').extract_first()
        company_str_list = re.sub('[\t\r\n \xa0]', '', company_str).split('|')
        for company_item in company_str_list:
            if '公司' in company_item or '合资' in company_item \
                or r'外资' in company_item or r'国企' in company_item \
                or r'单位' in company_item:
                item['company_type'] = company_item
            elif '人' in company_item and '0' in company_item:
                item['company_size'] = company_item
            else:
                item['company_area'] = company_item

        item['experience_requirement'] = response.xpath('//span[@class="sp4"][em[@class="i1"]]/text()').extract_first()
        item['education_requirement'] = response.xpath('//span[@class="sp4"][em[@class="i2"]]/text()').extract_first()
        item['recruiting_number'] = response.xpath('//span[@class="sp4"][em[@class="i3"]]/text()').extract_first()
        item['posted_date'] = response.xpath('//span[@class="sp4"][em[@class="i4"]]/text()').extract_first()
        job_tag_list = response.xpath('//div[@class="jtag inbox"]/p/span/text()').extract()
        item['job_tag'] = merge_string(job_tag_list, delimiter=",")

        position_info_list = response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()
        item['job_info'] = merge_string(position_info_list)
        company_info_list = response.xpath('//div[@class="tmsg inbox"]/text()').extract()
        item['company_info'] = merge_string(company_info_list)

        yield item