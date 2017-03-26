import scrapy
from job.items import JobItem
import re
from selenium import webdriver
import time


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


class LagouSpider(scrapy.Spider):
    name = "lagou"

    def start_requests(self):
        # search_fields = ['大数据', '数据分析', '数据运营', '数据挖掘']
        search_fields = ['大数据',]
        root_url = 'https://www.lagou.com'
        urls = []
        for field in search_fields:
            driver = webdriver.Chrome()  # open browser
            driver.get(root_url)  # open root url
            close_btn = driver.find_element_by_id('cboxClose')  # close city dialog box if found
            if close_btn is not None:
                close_btn.click()
            time.sleep(1)  # waiting for closing dialog
            driver.find_element_by_id('search_input').send_keys('%s' % field)
            driver.find_element_by_id('search_button').click()
            time.sleep(3)  # waiting for redirection
            position_links = driver.find_elements_by_class_name('position_link')
            for position_link in position_links:
                job_url = position_link.get_attribute('href')
                print('adding new seed url: %s' % job_url)
                urls.append(job_url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_job_info)

    def parse_job_info(self, response):
        url = response.url 
        site = url.split("//")[1].split('/')[0]
        print('parsing: %s' % response.url)
        if site == 'forbidden.lagou.com':  # exit if blocked
            print("Oh, I'm blocked.")
            return None

        item = JobItem()
        item['url'] = url 
        item['company_name'] = response.xpath('//div[@class="company"]/text()').extract_first()
        item['job_position'] = response.xpath('//div[@class="job-name"]/span[@class="name"]/text()').extract_first()
        job_requests = response.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        for job_request in job_requests:
            if 'k-' in job_request:
                item['salary'] = job_request
            elif '经验' in job_request:
                item['experience_requirement'] = job_request
            elif '学历' in job_request \
                or '大专' in job_request \
                or '本科' in job_request \
                or '硕士' in job_request \
                or '博士' in job_request:
                item['education_requirement'] = job_request
            elif '全职' in job_request \
                or '兼职' in job_request \
                or '实习' in job_request:
                item['job_type'] = job_request
            else:
                item['city'] = re.sub('[\ /]', '', job_request)
        # other field

        yield item
        # follow similar position links

