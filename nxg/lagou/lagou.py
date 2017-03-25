# -*- coding: utf-8 -*-
import urllib.request
import requests
import urllib.parse
import urllib.error
import http.cookiejar
import json
import datetime
import re
from threading import Thread
from time import sleep
from queue import Queue
from bs4 import BeautifulSoup
import openpyxl
import time
from grabutil.MysqlConnection import MysqlConnection


class LagouCrawler:
    def __init__(self, db, max_count=50, thread_num=5):
        """
        :param db: 数据库名（mysql）
        :param max_count: 批量插入数据库的条数
        :param thread_num:  并行线程数
        :return:
        """
        self.position_default_url = "http://www.lagou.com/jobs/"
        self.seed_url = 'http://www.lagou.com/zhaopin/'
        self.lagou_url = "http://www.lagou.com/"
        self.base_request_url = "http://www.lagou.com/jobs/positionAjax.json?city="
        self.proxies = [{"HTTP": "58.248.137.228:80"}, {"HTTP": "58.251.132.181:8888"}, {"HTTP": "60.160.34.4:3128"},
                        {"HTTP": "60.191.153.12:3128"}, {"HTTP": "60.191.164.22:3128"}, {"HTTP": "80.242.219.50:3128"},
                        {"HTTP": "86.100.118.44:80"}, {"HTTP": "88.214.207.89:3128"}, {"HTTP": "91.183.124.41:80"},
                        {"HTTP": "93.51.247.104:80"}]
        self.to_add_infos = []
        self.max_count = max_count  # 批量插入的记录数
        self.thread_num = thread_num  # 线程数
        self.job_queue = Queue()  # 任务队列
        self.new_come_company = []
        self.query = "insert into lagou.company(companyId, companyShortName, companyFullName,  financeStage, " \
            "city, industryField,companySize)" \
            " values (%s, %s, %s, %s,%s, %s, %s)"
        Cookie = 'JSESSIONID=E5247E45849AC75488AF0C6321A7C35D;LGRID=20170102170502-8b571b4d-d0ca-11e6-8ae7-525400f775ce;LGSID=20170102170435-7b95e1f1-d0ca-11e6-8aa2-5254005c3644;LGUID=20170102170435-7b95e514-d0ca-11e6-8aa2-5254005c3644;PRE_HOST=	.lagou.com;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;_ga=GA1.2.1488686692.1483348600;_gat=1;index_location_city=%E5%85%A8%E5%9B%BD;user_trace_token=20170102170435-44c6810993fb475b9e033826df9dfc48;'
        #20161226214035-355aa85d7b5b4f508a658453e446c3b2
        self.head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0','Cookie':Cookie}
        self.index = 0
        self.mysqlconn = MysqlConnection(db=db)
        self.my_opener = self.make_my_opener()
        self.start_thread()  # 开启多线程



    # 开启多线程
    def start_thread(self):
        for i in range(self.thread_num):
            curr_thread = Thread(target=self.working)
            curr_thread.setDaemon(True)
            curr_thread.start()

    def get_cooki(self):
        pass


    def make_my_opener(self):
        """
        模拟浏览器发送请求
        :return:
        """
        # proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        #cj = http.cookiejar.CookieJar()  # cookie

        opener = urllib.request.build_opener()
        header = []
        for key, value in self.head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header

        return opener

    def change_salary(self, salary):
        """
        :param salary: 处理拉钩的薪资
        :return:
        """
        salaries = re.findall("\d+", salary)
        if salaries.__len__() == 0:
            return 0, 0
        elif salaries.__len__() == 1:
            return int(salaries[0])*1000, int(salaries[0])*1000
        else:
            return int(salaries[0])*1000, int(salaries[1])*1000

    def position_detail(self, position_id):
        """
        处理职位详情
        :param position_id:
        :return:
        """

        position_url = self.position_default_url + str(position_id)+".html"
        print(position_url)
        op = self.my_opener.open(position_url, timeout=1000)
        detail_soup = BeautifulSoup(op.read().decode(), 'html.parser')
        job_company = detail_soup.find(class_='job_company')
        job_detail = detail_soup.find(id='job_detail')
        job_req = job_detail.find(class_='job_bt')
        c_feature = job_company.find(class_='c_feature')
        homePage = c_feature.find('a')
        homeUrl = homePage.get('href')
        return job_req, homeUrl

    def grab_city(self):
        """
        获取所有的城市
        :return:
        """
        print("开始获取所有城市")
        #op = self.my_opener.open(self.seed_url)

        #my_soup = BeautifulSoup(op.read().decode(), 'html.parser')
        #all_positions_html = my_soup.find(class_='more more-positions')
        #all_positions_hrefs = all_positions_html.find_all('a')
        all_cities = ['北京','上海','深圳','杭州','广州','成都','武汉','苏州','南京','厦门']
        #for a_tag in all_positions_hrefs:
        #        all_cities.append(a_tag.contents[0])
        #print("获取所有城市完成")
        return all_cities

    def grab_position(self):
        """
        获取所有招聘职位
        :return:
        """
        print("开始获取所有招聘职位")
        #html = self.my_opener.open(self.lagou_url)
        #soup = BeautifulSoup(html.read().decode(), "html.parser")
        #side_bar = soup.find(id="sidebar")
        #mainNavs = side_bar.find(class_="mainNavs")
        #menu_boxes = mainNavs.find_all(class_="menu_box")
        all_positions = ['医疗AI','医疗人工智能','自然语言处理','NLP','知识图谱','人工智能','AI','数据挖掘','大数据','推荐算法','精准医疗','深度学习','机器学习']
        #for menu_box in menu_boxes:
        #    menu_sub = menu_box.find(class_="menu_sub")  # 所有职位
        #    all_a_tags = menu_sub.find_all("a")  # 找出所有职位的a标签
        #    for a_tag in all_a_tags:
        #        all_positions.append(a_tag.contents[0])
        print("获取所有职位完成")
        return all_positions

    def write_to_excel(self,result,file_name):
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        filename=file_name
        for line in result:
            sheet.append(line)
        excel.save(filename)

    def insert_into_database(self, result):
        """
        插入数据
        :param result:待插入的抓取信息
        :return:
        """

        companyId = result['companyId']
        companyShortName = result['companyShortName']
        companyName = result['companyFullName']
        financeStage = result['financeStage']
        city = result['city']
        industryField = result['industryField']
        companySize = result['companySize']
        self.to_add_infos.append((str(companyId),companyShortName,companyName,financeStage,city,industryField,companySize))
        self.new_come_company.append((str(companyId),companyShortName,companyName,financeStage,city,industryField,companySize))
        if self.to_add_infos.__len__() >=0:   #self.max_count:  # 批量插入
            try:
                self.mysqlconn.execute_many(sql=self.query, args=self.to_add_infos)
                print("------------------insert successful---------------")
            except Exception:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!失败了！！！！！！！！！！！！！！！！！！！！！！！！！！！")
                pass
            self.to_add_infos.clear()  # 清空数据

    def working(self):
        while True:
            post_data = self.job_queue.get()  # 取任务
            try:
                self.grab(post_data)  # 抓取任务
            except Exception:
                print('here1')
            sleep(3)
            self.job_queue.task_done()

    def company_exist(self, companyId):

        sql = 'select * from company where companyId='+companyId
        res =self.mysqlconn.select_query(sql)
        if len(res) == 0:
            return False
        else:
            return True

    def grab(self, args):
        """
        根据参数args发请求，获取数据
        :param args:请求参数字典{'first': '？', 'kd': ？, 'city': ？, 'pn': ？}
        :return:
        """
        url = self.base_request_url + urllib.parse.quote(args['city'])
        url.encode(encoding='utf-8')
        print(url + "--------"+str(args))
        del args['city']  # 把city这个键删了，，，，不然，请求没有数据返回！！！
        #postdata = urllib.parse.urlencode({'px':'new','first': 'true', 'pn': pn,'kd':kd}).encode()
        post_data = urllib.parse.urlencode(args).encode()
        try:
            op = self.my_opener.open(url, post_data)
            return_json = json.loads(op.read().decode())
            #return_json = self.get_position_json(self,url,'false',args['kd'],args['pn'])
            content_json = return_json['content']
            total_page = round(content_json['positionResult']['totalCount']/content_json['pageSize'])
            result_list = content_json['positionResult']['result']

            for result in result_list:
                # 插入数据库啦
                print(result)
                companyId = str(result['companyId'])
                #company_exist(companyId)
                res = self.company_exist(companyId)
                if res:
                   continue
                else:
                    self.insert_into_database(result)
        except Exception as e :
            print(e)

    def grab_category(self, city, kd):
        """
        分类抓取
        :param city:当前城市
        :param kd: 当前职位类型
        :return:
        """

        url = self.base_request_url+urllib.parse.quote(city)
        url.encode(encoding='utf-8')
        pn = 1
        postdata = urllib.parse.urlencode({'px':'new','first': 'true', 'pn': pn,'kd':kd}).encode()
        pn += 1
        try:
            print(url, postdata)
            op = self.my_opener.open(url, postdata)
        except Exception:
            sleep(60)
            return
        return_json = json.loads(op.read().decode())
        content_json = return_json['content']
        total_page = round(content_json['positionResult']['totalCount']/content_json['pageSize'])
        result_list = content_json['positionResult']['result']
        for result in result_list:
            companyId = str(result['companyId'])
                #company_exist(companyId)
            res = self.company_exist(companyId)
            if res:
                continue
            else:
                self.insert_into_database(result)
        if total_page > 30:
            total_page = 30
        while pn <= total_page:
            # 一个任务处理一页
            self.job_queue.put({'px':'new','first': 'false', 'city': city, 'pn': pn,'kd':kd})
            pn += 1
            if self.job_queue.qsize() == 5:
                self.job_queue.join()
                #self.change_proxy()
        self.job_queue.join()

        print('successful')

    def start(self):
        print("开始抓取啦.............")
        all_cities = self.grab_city()
        all_positions = self.grab_position()

        for i in range(0, int(all_cities.__len__())):
            start_time = datetime.datetime.now()
            for j in range(0, int(all_positions.__len__())):

                grabed_cities_file = open("d:\\grabed3.txt", 'a')
                self.grab_category(city=all_cities[i], kd=all_positions[j])
                end_time = datetime.datetime.now()
                grabed_cities_file.write(all_cities[i]+"----职位："+all_positions[j]+"----耗时："
                                         + str((end_time-start_time).seconds)+"s\n")
                grabed_cities_file.close()
            end_time = datetime.datetime.now()
            grabed_cities_file = open("d:\\grabed1.txt", 'a')
            print((end_time-start_time).seconds)
            grabed_cities_file.write(all_cities[i]+"----耗时："+str((end_time-start_time).seconds)+"s\n")
            grabed_cities_file.close()

        self.write_to_excel(self.new_come_company,"lagouNewCompany.xlsx") #写入excel

        beifen_filename=time.strftime("d:\%Y%m%d_%H%M%S",time.localtime())+'.xlsx'   #在d盘备份
        self.write_to_excel(self.new_come_company,beifen_filename)
        if self.to_add_infos.__len__() != 0:    #万一不够50 这里还要把剩下的入库啊。 要不就丢了。
            try:
                self.mysqlconn.execute_many(sql=self.query, args=self.to_add_infos)
                print("------------------insert successful---------------")
            except Exception:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!失败了！！！！！！！！！！！！！！！！！！！！！！！！！！！")
                pass
        self.mysqlconn.close()

        print("----------抓取完啦--------------")


def main():
    my_crawler = LagouCrawler(db='lagou', max_count=50, thread_num=1)

    my_crawler.start()

if __name__ == '__main__':
    main()
