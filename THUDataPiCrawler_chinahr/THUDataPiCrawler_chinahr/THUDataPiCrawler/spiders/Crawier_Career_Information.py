import scrapy
from THUDataPiCrawler.items import ThudatapicrawlerItem


class CareerSpider(scrapy.Spider):
    name = 'THUDataPiCrawler_chinahr'
    allowed_domains = ["chinahr.com"]
    # log_url = ["https://www.zhipin.com/user/login.html?ka=header-login"]
    start_urls = ["http://www.chinahr.com/sou/?city=34%2C398&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 北京
                  "http://www.chinahr.com/sou/?city=36%2C400&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 上海
                  # "http://www.chinahr.com/job/5595829538654470.html",  # 数据分析 重庆
                  "http://www.chinahr.com/sou/?city=25%2C292&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 深圳
                  # "http://www.chinahr.com/job/5579147702010119.html",  # 数据分析 成都
                  "http://www.chinahr.com/sou/?city=25%2C291&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 广州
                  # "http://www.chinahr.com/job/5371965549775621.html",  # 数据分析 天津
                  # "http://www.chinahr.com/job/5468916234193155.html",  # 数据分析 苏州
                  # "http://www.chinahr.com/job/5449067762321668.html",  # 数据分析 郑州
                  # "http://www.chinahr.com/job/5465220097149958.html",  # 数据分析 武汉
                  # "http://www.chinahr.com/job/5596094828088325.html",  # 数据分析 杭州
                  # "http://www.chinahr.com/job/5561659736099332.html",  # 数据分析 石家庄
                  # "http://www.chinahr.com/job/5655119912111109.html",  # 数据分析 南京
                  # "http://www.chinahr.com/job/5204987724040710.html",  # 数据分析 沈阳
                  # "http://www.chinahr.com/job/5391799201237507.html",  # 数据分析 济南
                  # "http://www.chinahr.com/job/5561675290182145.html",  # 数据分析 长沙
                  # "http://www.chinahr.com/job/5562418888442369.html",  # 数据分析 西安
                  # "http://www.chinahr.com/job/5602039933468931.html",  # 数据分析 合肥
                  # "http://www.chinahr.com/job/5609920456231171.html",  # 数据分析 青岛
                  # "http://www.chinahr.com/job/5565921948338433.html",  # 数据分析 东莞
                  # "http://www.chinahr.com/job/5590722055309569.html",  # 数据分析 哈尔滨
                  # "http://www.chinahr.com/job/5595905662650885.html",  # 数据分析 大连
                  # "http://www.chinahr.com/job/5366499646702081.html",  # 数据分析 长春
                  # "http://www.chinahr.com/job/5590137686035460.html",  # 数据分析 中山
                  # "http://www.chinahr.com/job/5567883032464129.html",  # 数据分析 佛山
                  # "http://www.chinahr.com/job/5590676239879172.html",  # 数据分析 南宁
                  # "http://www.chinahr.com/job/5466497922859527.html",  # 数据分析 无锡
                  # "http://www.chinahr.com/job/5576326270454790.html",  # 数据分析 贵阳
                  # "http://www.chinahr.com/job/5590207402510596.html",  # 数据分析 宁波
                  # "http://www.chinahr.com/job/5649318463933446.html",  # 数据分析 福州
                  # "http://www.chinahr.com/job/5595718663440896.html",  # 数据分析 太原
                  # "http://www.chinahr.com/job/5590174295165442.html",  # 数据分析 保定
                  # "http://www.chinahr.com/job/5590805658765828.html",  # 数据分析 南昌
                  # "http://www.chinahr.com/job/5596105698413062.html",  # 数据分析 厦门
                  # "http://www.chinahr.com/job/5596035842083328.html",  # 数据分析 常州
                  # "http://www.chinahr.com/job/5590426972553730.html",  # 数据分析 珠海
                  # "http://www.chinahr.com/job/5329510687083009.html",  # 数据分析 烟台
                  # "http://www.chinahr.com/job/5566287864824323.html",  # 数据分析 昆明
                  # "http://www.chinahr.com/job/5587847354289152.html",  # 数据分析 海口
                  # "http://www.chinahr.com/job/5366538190062080.html",  # 数据分析 廊坊
                  # "http://www.chinahr.com/job/5596053920612615.html",  # 数据分析 潍坊
                  # "http://www.chinahr.com/job/5505174190227970.html",  # 数据分析 乌鲁木齐
                  # "http://www.chinahr.com/job/5343607307406082.html",  # 数据分析 呼和浩特
                  # "http://www.chinahr.com/job/5566279686818310.html",  # 数据分析 徐州
                  # "http://www.chinahr.com/job/5527838642571523.html",  # 数据分析 兰州
                  ]
    base_url = "http://www.chinahr.com/sou/?"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_career_list)

    def parse_career_list(self, response):
        research_list_urls = ''.join(scrapy.Selector(response).xpath('//*[@id="searchList"]/div[2]/div/@data-url').extract()).split('http://')[1:]
        next_url = self.base_url + ''.join(scrapy.Selector(response).xpath('//*[@class="pageList"]/a/@href').extract()).split('?')[-1]
        # print(next_url)
        yield scrapy.Request(url=next_url, callback=self.parse_career_list)
        for url in research_list_urls:
            yield scrapy.Request(url="http://" + url, callback=self.parse_career_information)


    def parse_career_information(self, response):
        job_title = ''.join(scrapy.Selector(response).xpath('//*[@class="job_name"]/text()').extract())
        if ('数据' in job_title) or ('数据分析' in job_title) or ('大数据' in job_title)\
                or ('爬虫' in job_title) or ('数据分析' in job_title) or ('数据抓取' in job_title)\
                or ('数据可视化' in job_title) or ('Hadoop' in job_title) or ('Spark' in job_title) \
                or ('hbase' in job_title) or ('hive' in job_title) or ('hadoop' in job_title) \
                or ('spark' in job_title):
            item = ThudatapicrawlerItem()
            item['Company_Name'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job-company jrpadding"]/h4/a/text()').extract()).replace('\xa0', '')
            # print(item['Company_Name'])
            item['Job_Title'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_name"]/text()').extract())
            # print(item['Job_Title'])
            item['Job_Labels'] = 'NULL'          # 信息缺失
            item['Department_Name'] = 'NULL'     # 信息缺失
            item['Company_Profile'] = 'NULL'     # 信息缺失
            item['Company_Label'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[1]/text()').extract()).replace(' ', '').replace('\r', '').replace('\n', '')
            # print(item['Company_Label'])
            item['Company_Size'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[3]/text()').extract())
            # print(item['Company_Size'])
            if '人' in item['Company_Size']:
                item['Company_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[2]/text()').extract())
                # print(item['Company_Type'])
                # print(item['Company_Size'])
            else:
                item['Company_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[3]/text()').extract())
                item['Company_Size'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[4]/text()').extract())
                # print(item['Company_Type'])
                # print(item['Company_Size'])
            item['Financing_Stage'] = 'NULL'     # 信息缺失
            item['Company_Home_Page'] = 'NULL'
            item['Work_Place'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_loc"]/text()').extract())
            # print(item['Work_Place'])
            item['Salary'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_price"]/text()').extract())
            # print(item['Salary'])
            item['Job_Highlights'] = ''.join(scrapy.Selector(response).xpath('//*[@class="clear"]/li').extract())
            # print(item['Job_Highlights'])
            item['Job_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]/span[3]/text()').extract())
            # print(item['Job_Type'])
            item['Experience'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_exp"]/text()').extract())
            # print(item['Experience'])
            item['Education'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]/span[4]/text()').extract())
            # print(item['Education'])
            item['Job_Description_and_Job_Requirements'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_intro_info"]').extract())
            # print(item['Job_Description_and_Job_Requirements'])
            item['Release_Time'] = ''.join(scrapy.Selector(response).xpath('//*[@class="updatetime"]/text()').extract())
            # print(item['Release_Time'])
            item['Source_Site'] = ''.join(scrapy.Selector(response).xpath('//*[@id="yc_tnav"]/div/div[1]/a/text()').extract()).replace('\xa0', '').replace('\u2764', '')
            # print(item['Source_Site'])
            yield item
