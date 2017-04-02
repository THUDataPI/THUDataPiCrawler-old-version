#!/bin/env python

"""字段格式转换；职位过滤；sqlite数据库转换为xlsx。
Usage:
    sql2xlsx.py -i sqlite.db [options]

Options:
    -h --help                           Show this screen.
    -i sqlite.db                        Specified sqlite database to process.
    -o output.xlsx                      Specified filename of output xlsx file [default: output.xlsx].
    -t table                            Specified table to process [default: qcwy].
    -k keyword.txt                      Specified keyword file for position filtering [default: ../keyword.txt].
    --show-rejected=<show_rejected>     Show rejected positions or not [default: False].
"""

import pandas as pd 
import sqlite3
import re
from docopt import docopt
from tqdm import tqdm
from openpyxl import Workbook


def get_salary(salary_str):
    """薪资转换为以“元”为单位的月薪
    
    Args:
        salary_str (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    unit_dict = {'元': 1, '千': 1E3, '万': 1E4}
    period_dict = {'小时': 720., '天': 30., '月': 1, '年': 1./12.}
    if salary_str is None:
        return "0-0"
    salary_str = re.sub('[以+上下\ ]', '', salary_str)  # 去掉“以上、以下、+”特殊字符
    values, period = salary_str.split('/')
    unit = values[-1]  # 工资单位：元，千，万
    n0_1 = values[:-1].split('-')
    n0 = float(n0_1[0]) * unit_dict[unit] * period_dict[period]
    if len(n0_1) == 2:
        n1 = float(n0_1[1]) * unit_dict[unit] * period_dict[period]
    else:
        n1 = n0
    formated_salary_str = '%d-%d' % (n0, n1)
    return formated_salary_str


def get_recruiting_number(recruiting_str):
    if '若干' in recruiting_str:
        return '-1'
    else:
        return re.sub('[招聘人]', '', recruiting_str)


def get_company_size(size_str):
    if size_str == '少于50人':
        return '1-50人'
    elif size_str == '10000人以上':
        return '10000-100000人'
    else:
        return size_str


def get_posted_date(data_str):
    return '2017/4/1'  # 前程无忧招聘信息发布时间为爬取时间，无任何意义！


def get_city(s):
    if s == '' or s is None:
        return 'NULL'
    else:
        return s


def get_experience(s):
    if s == '' or s is None:
        return 'NULL'
    else:
        return s


def get_education(s):
    if s == '' or s is None:
        return 'NULL'
    else:
        return s


def get_position_advantage(s):
    if s == '' or s is None:
        return 'NULL'
    else:
        return s


def load_keyword(filepath):
    f = open(filepath, 'r')
    keywords = f.readlines()
    f.close()
    for i in range(len(keywords)):
        keywords[i] = re.sub('\n', '', keywords[i])
    return keywords


field_dict = {'position': '职位名称',
              'position_tag': '职位分类标签',
              'department': '部门',
              'city': '工作地点',
              'position_type': '工作性质',
              'experience_requirement': '经验',
              'education_requirement': '学历',
              'salary': '薪资',
              'major_requirement': '专业要求',
              'recruiting_number': '招聘人数',
              'position_advantage': '职位诱惑',
              'position_info': '岗位介绍',
              'company': '公司名称',
              'company_industry': '公司行业',
              'company_type': '公司性质',
              'company_finance': '融资阶段',
              'company_size': '公司规模',
              'company_url': '公司主页',
              'posted_date': '发布日期',
              'posted_website': '发布网站',
              'posted_url': '原始URL'}


if __name__ == '__main__':
    # parse argments
    args = docopt(__doc__)
    sqlite_file = args['-i']
    table = args['-t']
    output = args['-o']
    keywords = load_keyword(args['-k'])
    show_rejected = args['--show-rejected']
    print('%s:%s -> %s with keywords:\n%s' 
          % (sqlite_file, table, output, keywords))

    # create xlsx workbook and header
    wb = Workbook()
    ws = wb.active
    ws.append([field_dict['position'],
               field_dict['position_tag'],
               field_dict['department'],
               field_dict['city'],
               field_dict['position_type'],
               field_dict['experience_requirement'],
               field_dict['education_requirement'],
               field_dict['salary'],
               field_dict['major_requirement'],
               field_dict['recruiting_number'],
               field_dict['position_advantage'],
               field_dict['position_info'],
               field_dict['company'],
               field_dict['company_industry'],
               field_dict['company_type'],
               field_dict['company_finance'],
               field_dict['company_size'],
               field_dict['company_url'],
               field_dict['posted_date'],
               field_dict['posted_website'],
               field_dict['posted_url']])
    # load sqlite database, write the filterd position to xlsx
    con = sqlite3.connect(sqlite_file)
    df = pd.read_sql_query("SELECT * from %s" % table, con)
    nb_jobs = df.shape[0]
    nb_accepted_jobs = 0
    rejected_jobs = []
    for i in tqdm(range(nb_jobs)):
        position = df.iloc[i]['position']
        accepted = False
        for keyword in keywords:
            if keyword in position:
                try:
                    ws.append([df.iloc[i]['position'],
                               df.iloc[i]['position_tag'],
                               df.iloc[i]['department'],
                               get_city(df.iloc[i]['city']),
                               df.iloc[i]['position_type'],
                               get_experience(df.iloc[i]['experience_requirement']),
                               get_education(df.iloc[i]['education_requirement']),
                               get_salary(df.iloc[i]['salary']),
                               df.iloc[i]['major_requirement'],
                               get_recruiting_number(df.iloc[i]['recruiting_number']),
                               get_position_advantage(df.iloc[i]['position_advantage']),
                               df.iloc[i]['position_info'],
                               df.iloc[i]['company'],
                               df.iloc[i]['company_industry'],
                               df.iloc[i]['company_type'],
                               df.iloc[i]['company_finance'],
                               get_company_size(df.iloc[i]['company_size']),
                               df.iloc[i]['company_url'],
                               get_posted_date(df.iloc[i]['posted_date']),
                               df.iloc[i]['posted_website'],
                               df.iloc[i]['posted_url']])
                    nb_accepted_jobs += 1
                except Exception as e:
                    print(e)
                    continue
                accepted = True
                break
        if accepted == False:
            rejected_jobs.append(position)
    wb.save(output)  # save xlsx workbook
    print('='*60)
    print('Total accepted position: %d/%d' % (nb_accepted_jobs, nb_jobs))
    if show_rejected == 'True':
        print('Rejected %d jobs: %s' % (len(rejected_jobs), rejected_jobs))
    print('='*60)