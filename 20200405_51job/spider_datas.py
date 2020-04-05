#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
from lxml import etree
import pandas as pd
import time
import random
import csv
import re


headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Cookie":"******"
}

url_list=[]
with open('urls.txt','r',encoding="utf-8") as f:
    for i in f.readlines():
        i=i.strip()
        url_list.append(i)

def spider():
    count=1

    info_list=[]
    for i in range(len(url_list)):

        # 数据我们只取10000条
        if i==10050:
            break

        try:
            print("正在解析第{}条".format(i+1))

            response = requests.get(url_list[i], headers=headers)

            response.encoding = "gbk"

            html = response.text

            root = etree.HTML(html)

            # 1.岗位名称
            job_name = root.xpath('string(//div[@class="cn"]/h1/@title)')

            # 2.公司名称
            company_name = root.xpath('string(//div[@class="cn"]/p/a/@title)')

            random_all = root.xpath('//div[@class="cn"]//p[@class="msg ltype"]/text()')
            random_all = [i.replace('\xa0', '').strip() for i in random_all]

            # 3.工作地点
            address = random_all[0]

            # 4.工资
            salary_mid = root.xpath('string(//div[@class="cn"]/strong/text())')
            salary = salary_mid if salary_mid else '-'

            # 5.发布时间
            release = "".join(random_all)
            release_time = re.findall('\d+-\d+',release)[-1]

            # 6.混合数据(经验，学历等)
            random_all = root.xpath('//div[@class="cn"]/p[@class="msg ltype"]/text()')
            random_all = [i.replace('\xa0','').strip() for i in random_all]

            # 7.岗位描述信息
            job_drscribe = root.xpath('string(//div[@class="bmsg job_msg inbox"])').replace("\xa0", "").replace("\r\n","").strip()

            # 8.公司类型
            company_type = root.xpath('string(//div[@class="com_tag"]/p[1]/@title)')

            # 9.公司规模
            company_size = root.xpath('string(//div[@class="com_tag"]/p[2]/@title)')

            # 10.所属行业
            industry = root.xpath('string(//div[@class="com_tag"]/p[3]/@title)')

            info_list.append([job_name,company_name,address,salary,release_time,random_all,company_type,company_size,industry,job_drscribe])

            time.sleep(random.randint(3, 5))

        except Exception as e:
            print(e)

    # 写入csv
    with open('job_info1.csv', 'a', encoding='gbk', newline='') as csvFile:
        csv.writer(csvFile).writerow(['岗位名称','公司名称','工作地点','工资','发布时间','要求','公司类型','公司规模','所属行业',"岗位描述"])
        for rows in info_list:
            csv.writer(csvFile).writerow(rows)

if __name__=="__main__":
    spider()

