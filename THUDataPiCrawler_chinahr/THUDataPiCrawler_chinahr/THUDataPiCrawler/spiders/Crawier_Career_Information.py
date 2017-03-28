import scrapy
from THUDataPiCrawler.items import ThudatapicrawlerItem


class CareerSpider(scrapy.Spider):
    name = 'THUDataPiCrawler_chinahr'
    allowed_domains = ["chinahr.com"]
    # log_url = ["https://www.zhipin.com/user/login.html?ka=header-login"]
    start_urls = [# "http://www.chinahr.com/sou/?city=34%2C398&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96",   # 数据可视化 北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=hadoop",  # hadoop 北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=spark",   # spark 北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86",  # 产品经理（数据方向）北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE",  # 大数据 北京
                  # "http://www.chinahr.com/sou/?city=34%2C398&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 北京

                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 上海
                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=hadoop",  # Hadoop 上海
                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=spark",  # spark 上海
                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E6%95%B0%E6%8D%AE",  # 产品经理（数据方向） 上海
                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 上海
                  # "http://www.chinahr.com/sou/?city=36%2C400&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE",  # 大数据 上海

                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 深圳+广州
                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=hadoop",  # hadoop 深圳+广州
                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=spark",   # spark 深圳+广州
                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E6%95%B0%E6%8D%AE",  # 产品经理（数据方向）深圳+广州
                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE",  # 大数据 深圳+广州
                  # "http://www.chinahr.com/sou/?city=25%2C291%3B25%2C292&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 深圳+广州

                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 苏州+杭州+南京
                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=hadoop",  # hadoop 苏州+杭州+南京
                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=spark",   # spark 苏州+杭州+南京
                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E6%95%B0%E6%8D%AE",  # 产品经理（数据方向）苏州+杭州+南京
                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE",  # 大数据 苏州+杭州+南京
                  "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 苏州+杭州+南京

                  # "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 重庆+成都+天津
                  # "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=hadoop",  # hadoop 重庆+成都+天津
                  # "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=spark",  # spark 重庆+成都+天津
                  # "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E6%95%B0%E6%8D%AE",  # 产品经理（数据方向）重庆+成都+天津
                  # "http://www.chinahr.com/sou/?city=17%2C182%3B16%2C173%3B16%2C169&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 重庆+成都+天津
                  # "http://www.chinahr.com/job/5595829538654470.html",  # 数据分析 重庆+成都+天津

                  # "http://www.chinahr.com/sou/?city=25%2C307%3B25%2C296%3B25%2C308%3B25%2C293&keyword=hadoop",  # hadoop 东莞+佛山+中山+珠海
                  # "http://www.chinahr.com/sou/?city=25%2C307%3B25%2C296%3B25%2C308%3B25%2C293&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 东莞+佛山+中山+珠海
                  # "http://www.chinahr.com/sou/?city=25%2C307%3B25%2C296%3B25%2C308%3B25%2C293&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 东莞+佛山+中山+珠海

                  # "http://www.chinahr.com/sou/?city=17%2C183%3B16%2C170%3B16%2C172%3B19%2C210%3B19%2C211&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 无锡+宁波+常州+福州+厦门
                  # "http://www.chinahr.com/sou/?city=17%2C183%3B16%2C170%3B16%2C172%3B19%2C210%3B19%2C211&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 无锡+宁波+常州+福州+厦门
                  # "http://www.chinahr.com/sou/?city=17%2C183%3B16%2C170%3B16%2C172%3B19%2C210%3B19%2C211&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 无锡+宁波+常州+福州+厦门

                  # "http://www.chinahr.com/sou/?city=24%2C277%3B20%2C219%3B22%2C249%3B23%2C264&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 长沙+南昌+武汉+洛阳
                  # "http://www.chinahr.com/sou/?city=24%2C277%3B20%2C219%3B22%2C249%3B23%2C264&keyword=%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86",  # 产品经理（数据方向）长沙+南昌+武汉+洛阳
                  # "http://www.chinahr.com/sou/?city=24%2C277%3B20%2C219%3B22%2C249%3B23%2C264&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 长沙+南昌+武汉+洛阳
                  # "http://www.chinahr.com/sou/?city=24%2C277%3B20%2C219%3B22%2C249%3B23%2C264&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 长沙+南昌+武汉+洛阳

                  # "http://www.chinahr.com/sou/?city=30%2C358%3B22%2C247%3B31%2C368&keyword=hadoop",  # hadoop 西安+郑州+兰州
                  # "http://www.chinahr.com/sou/?city=30%2C358%3B22%2C247%3B31%2C368&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 西安+郑州+兰州
                  # "http://www.chinahr.com/sou/?city=30%2C358%3B22%2C247%3B31%2C368&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 西安+郑州+兰州

                  # "http://www.chinahr.com/sou/?city=18%2C193%3B28%2C333%3B16%2C171%3B38%2C402%3B41%2C435&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 合肥+徐州+南宁+贵阳+银川
                  # "http://www.chinahr.com/sou/?city=18%2C193%3B28%2C333%3B16%2C171%3B38%2C402%3B41%2C435&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 合肥+徐州+南宁+贵阳+银川
                  # "http://www.chinahr.com/sou/?city=18%2C193%3B28%2C333%3B16%2C171%3B38%2C402%3B41%2C435&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 合肥+徐州+南宁+贵阳+银川

                  # "http://www.chinahr.com/sou/?city=15%2C156%3B13%2C134%3B14%2C147%3B13%2C133&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 大连+长春+哈尔滨+沈阳
                  # "http://www.chinahr.com/sou/?city=15%2C156%3B13%2C134%3B14%2C147%3B13%2C133&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 大连+长春+哈尔滨+沈阳
                  # "http://www.chinahr.com/sou/?city=15%2C156%3B13%2C134%3B14%2C147%3B13%2C133&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 大连+长春+哈尔滨+沈阳

                  # "http://www.chinahr.com/sou/?city=11%2C111%3B12%2C122%3B11%2C116&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 石家庄+太原+保定
                  # "http://www.chinahr.com/sou/?city=11%2C111%3B12%2C122%3B11%2C116&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 石家庄+太原+保定

                  # "http://www.chinahr.com/sou/?city=26%2C309%3B29%2C342%3B42%2C440%3B39%2C416&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 海口+昆明+乌鲁木齐+呼和浩特
                  # "http://www.chinahr.com/sou/?city=26%2C309%3B29%2C342%3B42%2C440%3B39%2C416&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 海口+昆明+乌鲁木齐+呼和浩特

                  # "http://www.chinahr.com/sou/?city=21%2C231%3B21%2C235%3B11%2C120%3B21%2C236%3B21%2C230&keyword=%E7%88%AC%E8%99%AB",  # 爬虫 济南+廊坊+烟台+潍坊+青岛
                  # "http://www.chinahr.com/sou/?city=21%2C231%3B21%2C235%3B11%2C120%3B21%2C236%3B21%2C230&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE"  # 大数据 济南+廊坊+烟台+潍坊+青岛
                  # "http://www.chinahr.com/sou/?city=21%2C231%3B21%2C235%3B11%2C120%3B21%2C236%3B21%2C230&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90",  # 数据分析 济南+廊坊+烟台+潍坊+青岛
                  ]
    base_url = "http://www.chinahr.com/sou/?"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_career_list)

    def parse_career_list(self, response):
        research_list_urls = ''.join(scrapy.Selector(response).xpath('//*[@id="searchList"]/div[2]/div/@data-url').extract()).split('http://')[1:]
        next_url = self.base_url + ''.join(scrapy.Selector(response).xpath('//*[@class="pageList"]/a/@href').extract()).split('?')[-1]
        # print(next_url)
        if ('city=' in next_url) and ('keyword=' in next_url):
            yield scrapy.Request(url=next_url, callback=self.parse_career_list)
        for url in research_list_urls:
            yield scrapy.Request(url="http://" + url, callback=self.parse_career_information)

    def parse_career_information(self, response):
        job_title = ''.join(scrapy.Selector(response).xpath('//*[@class="job_name"]/text()').extract())
        if ('数据' in job_title) or ('数据分析' in job_title) or ('大数据' in job_title)\
                or ('爬虫' in job_title) or ('大数据分析' in job_title) or ('数据抓取' in job_title)\
                or ('数据可视化' in job_title) or ('Hadoop' in job_title) or ('Spark' in job_title) \
                or ('hadoop' in job_title) or ('spark' in job_title):
            item = ThudatapicrawlerItem()
            item['Company_Name'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job-company jrpadding"]/h4/a/text()').extract()).replace('\xa0', '')
            item['Job_Title'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_name"]/text()').extract())
            item['Job_Labels'] = 'NULL'          # 信息缺失
            item['Department_Name'] = 'NULL'     # 信息缺失
            item['Major'] = 'NULL'               # 专业要求
            item['Number'] = 'NULL'              # 招聘人数
            item['Company_Label'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[1]/text()').extract()).replace(' ', '').replace('\r', '').replace('\n', '').replace('/', ',')
            item['Company_Size'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[3]/text()').extract()).replace('规模', '')
            if '人' in item['Company_Size']:
                item['Company_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[2]/text()').extract()).replace('/', '')
            else:
                item['Company_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[3]/text()').extract()).replace('/', '')
                item['Company_Size'] = ''.join(scrapy.Selector(response).xpath('//*[@class="compny_tag"]/span[4]/text()').extract()).replace('规模', '')
            item['Financing_Stage'] = 'NULL'     # 信息缺失
            item['Company_Home_Page'] = 'NULL'
            item['Work_Place'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_loc"]/text()').extract())
            item['Salary'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_price"]/text()').extract())
            if len(item['Salary']) < 4:  # 网站本身信息有误 直接舍弃
                return
            item['Job_Highlights'] = ''.join(scrapy.Selector(response).xpath('//*[@class="clear"]/li').extract()).replace('\xa0', '')
            item['Job_Type'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]/span[3]/text()').extract())
            item['Experience'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]//*[@class="job_exp"]/text()').extract())
            item['Education'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_require"]/span[4]/text()').extract())
            if len(item['Education']) == 0:
                item['Education'] = 'NULL'
            item['Job_Description_and_Job_Requirements'] = ''.join(scrapy.Selector(response).xpath('//*[@class="job_intro_info"]').extract()).replace('\xa0', '').replace('\u200b', '').replace('\uf0d8', '').replace('\u3000', '')
            item['Release_Time'] = ''.join(scrapy.Selector(response).xpath('//*[@class="updatetime"]/text()').extract())
            item['Source_Site'] = ''.join(scrapy.Selector(response).xpath('//*[@id="yc_tnav"]/div/div[1]/a/text()').extract()).replace('\xa0', '').replace('\u2764', '')
            item['Source_URL'] = response.url.replace('\xa0', '').replace('\u200b', '')
            yield item
