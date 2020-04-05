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

local_files=open("urls.txt","w",encoding="utf-8")

for i in range(1,675):

    print("正在爬取第{}页".format(i))

    url1=base_url.format(i)

    response1=requests.get(url1,headers=headers)

    response1.encoding="gbk"

    html=response1.text

    root1=etree.HTML(html)

    # 二级url
    deep_url = root1.xpath('//div[@class="el"]//p/span/a[@target="_blank"]/@href')

    for i in deep_url:

        local_files.write(i+"\n")

    time.sleep(random.randint(3, 5))


local_files.close()