#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
from lxml import etree
import pandas as pd
import time
import random


headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Cookie":"******"
}

base_url="https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="


for i in range(18,677):

    print("正在爬取第{}页".format(i))

    url1=base_url.format(i)

    response1=requests.get(url1,headers=headers)

    response1.encoding="gbk"

    html=response1.text

    root1=etree.HTML(html)

    # 1.岗位名称
    job_name = root1.xpath('//div[@class="el"]//p/span/a[@target="_blank"]/@title')

    # 2.公司名称
    company_name = root1.xpath('//div[@class="el"]/span[@class="t2"]/a[@target="_blank"]/@title')

    # 3.工作地点
    address = root1.xpath('//div[@class="el"]/span[@class="t3"]/text()')

    # 4.工资
    salary_mid = root1.xpath('//div[@class="el"]/span[@class="t4"]')
    salarys = [i.text for i in salary_mid]
    salary = [i if i else '-' for i in salarys]

    # 5.发布时间
    release_time = root1.xpath('//div[@class="el"]/span[@class="t5"]/text()')

    # 6.二级url
    deep_url = root1.xpath('//div[@class="el"]//p/span/a[@target="_blank"]/@href')

    RandomAll=[]
    JobDescribe=[]
    CompanyType=[]
    CompanySize=[]
    Industry=[]

    for url in deep_url:

        response2=requests.get(url,headers=headers)

        response2.encoding="gbk"

        html2=response2.text

        root2=etree.HTML(html2)

        # 7.混合数据(经验，学历等)
        random_all = root2.xpath('//div[@class="cn"]/p[@class="msg ltype"]/text()')

        # 8.岗位描述信息
        job_drscribe = root2.xpath('string(//div[@class="bmsg job_msg inbox"])').replace("\xa0","").replace("\r\n", "").strip()

        # 9.公司类型
        company_type = root2.xpath('string(//div[@class="com_tag"]/p[1]/@title)')

        # 10.公司规模
        company_size = root2.xpath('string(//div[@class="com_tag"]/p[2]/@title)')

        # 11.所属行业
        industry = root2.xpath('string(//div[@class="com_tag"]/p[3]/@title)')

        RandomAll.append(random_all)
        JobDescribe.append(job_drscribe)
        CompanyType.append(company_type)
        CompanySize.append(company_size)
        Industry.append(industry)

        time.sleep(random.randint(2,4))

    # 分步保存数据，防止最后一次性保存所有数据出现错误
    df=pd.DataFrame()
    df['岗位名称']=job_name
    df['公司名称']=company_name
    df['工作地点']=address
    df['工资']=salary
    df['发布时间']=release_time
    df['要求']=RandomAll
    df['公司类型']=CompanyType
    df['公司规模']=CompanySize
    df['所属行业']=Industry
    df["岗位描述"]=JobDescribe

    try:
        df.to_csv("job_info.csv",mode="a+",header=None,index=None,encoding='gbk')
    except:
        print("第{}页数据写入失败".format(i))


print("数据爬取完毕")

