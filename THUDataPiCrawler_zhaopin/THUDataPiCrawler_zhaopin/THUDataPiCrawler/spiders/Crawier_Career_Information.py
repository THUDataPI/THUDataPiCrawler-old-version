import scrapy
from THUDataPiCrawler.items import ThudatapicrawlerItem


class CareerSpider(scrapy.Spider):
    name = 'THUDataPiCrawler_jobs_zhaopin'
    allowed_domains = ["zhaopin.com"]
    # log_url = ["https://www.zhipin.com/user/login.html?ka=header-login"]
    start_urls =[
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1&isadv=0",    # 数据分析
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&p=1&isadv=0",             # 大数据
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&p=1&isadv=0",   # 数据产品经理
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E8%BF%90%E8%90%A5&p=1&isadv=0",  # 数据运营
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E7%88%AC%E8%99%AB&p=1&isadv=0", # 爬虫
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96&p=1&isadv=0", # 数据可视化
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=hadoop&p=1&isadv=0", # Hadoop
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=spark&p=1&isadv=0", # spark
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=hive&p=1&isadv=0",  # hive
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=hbase&p=1&isadv=0",  # hbase
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&p=1&isadv=0",  # 数据挖掘
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6&p=1&isadv=0",  # 数据科学家
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E5%B7%A5%E7%A8%8B&p=1&isadv=0",  # 数据工程师
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E6%9E%B6%E6%9E%84&p=1&isadv=0",  # 数据架构师
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_career_list)

    def parse_career_list(self, response):
        research_list_urls = ''.join(scrapy.Selector(response).xpath('//*[@class="zwmc"]/div/a/@href').extract()).split('http://')[1:]
        # print(research_list_urls)
        next_url = ''.join(scrapy.Selector(response).xpath('//*[@class="pagesDown-pos"]/a/@href').extract())#.split('?')[-1]
        print(next_url)
        if ('jl=' in next_url) and ('kw=' in next_url):
            yield scrapy.Request(url=next_url, callback=self.parse_career_list)
        for url in research_list_urls:
            # print(url)
            yield scrapy.Request(url="http://" + url, callback=self.parse_career_information)

    def parse_career_information(self, response):
        job_title = ''.join(scrapy.Selector(response).xpath('//*[@class="inner-left fl"]/h1/text()').extract())
        # print(job_title)
        if ('数据' in job_title) or ('数据分析' in job_title) or ('大数据' in job_title)\
                or ('爬虫' in job_title) or ('大数据分析' in job_title) or ('数据抓取' in job_title)\
                or ('数据可视化' in job_title) or ('Hadoop' in job_title) or ('Spark' in job_title) \
                or ('hadoop' in job_title) or ('spark' in job_title):
            item = ThudatapicrawlerItem()
            item['Company_Name'] = ''.join(scrapy.Selector(response).xpath('//*[@class="inner-left fl"]/h2/a/text()').extract()).replace('\xa0', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Company_Name'])
            item['Job_Title'] = ''.join(scrapy.Selector(response).xpath('//*[@class="inner-left fl"]/h1/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Job_Title'])
            item['Job_Labels'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract()).replace('/', ',').encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Job_Labels'])
            item['Department_Name'] = 'NULL'     # 信息缺失
            item['Major'] = 'NULL'               # 专业要求
            item['Number'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[7]/strong/text()').extract()).replace('人', '').encode('GBK', 'ignore').decode('GBK', 'ignore')             # 招聘人数
            # print(item['Number'])
            item['Company_Label'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[3]/strong/a/text()').extract()).replace('/', ',').encode('GBK', 'ignore').decode('GBK', 'ignore')# .replace(' ', '').replace('\r', '').replace('\n', '')
            # print(item['Company_Label'])
            item['Company_Size'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')# .replace('规模', '')
            # print(item['Company_Size'])
            item['Company_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[2]/strong/text()').extract()).replace('/', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Company_Type'])
            item['Financing_Stage'] = 'NULL'     # 信息缺失
            item['Company_Home_Page'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/a/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            if 'http' in item['Company_Home_Page']:
                pass
            else:
                item['Company_Home_Page'] = 'NULL'
            # print(item['Company_Home_Page'])
            item['Work_Place'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[2]/strong/a/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore') + ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[2]/strong/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Work_Place'])
            item['Salary'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()).replace('\xa0', '').replace('元/月', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Salary'])
            item['Job_Highlights'] = ''.join(scrapy.Selector(response).xpath('//*[@class="welfare-tab-box"]/span').extract()).replace('\xa0', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Job_Highlights'])
            item['Job_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[4]/strong/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Job_Type'])
            item['Experience'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Experience'])
            item['Education'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Education'])
            item['Job_Description_and_Job_Requirements'] = ''.join(scrapy.Selector(response).xpath('//*[@class="tab-inner-cont"]').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore') # .replace('\xa0', '').replace('\u200b', '').replace('\uf0d8', '').replace('\u3000', '').replace('\u273f', '')
            # print(item['Job_Description_and_Job_Requirements'])
            item['Release_Time'] = ''.join(scrapy.Selector(response).xpath('//*[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Release_Time'])
            item['Source_Site'] = ''.join(scrapy.Selector(response).xpath('//*[@class="all_navcontent"]/a/@title').extract()).encode('GBK', 'ignore').decode('GBK', 'ignore') # .replace('\xa0', '').replace('\u2764', '')
            # print(item['Source_Site'])
            item['Source_URL'] = response.url.encode('GBK', 'ignore').decode('GBK', 'ignore')
            # print(item['Source_URL'])
            yield item

