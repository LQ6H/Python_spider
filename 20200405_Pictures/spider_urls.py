#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
from lxml import etree
import time
import random
import os


headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}

local_file=open("urls.txt","a",encoding="utf-8")

base_url="http://pic.netbian.com/4kmeinv/index_{}.html"

for page in range(1, 196):
    print("正在爬取第{}页".format(page))

    url = "http://pic.netbian.com/4kmeinv/index.html"

    if page != 1:
        url = base_url.format(page)

    response = requests.get(url, headers=headers)
    response.encoding = "gbk"
    html = response.text
    root = etree.HTML(html)

    imgs_link = root.xpath('//ul[@class="clearfix"]/li/a/img/@src')



    for i in imgs_link:

        local_file.write("http://pic.netbian.com" + i+"\n")

    time.sleep(random.randint(2,5))
