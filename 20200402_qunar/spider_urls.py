#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import random


local_file=open("urls.txt","w",encoding="utf-8")

headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "cookie":"******",
    "referer":"https://travel.qunar.com/travelbook/list.htm?page=1&order=hot_heat"
}

base_url="https://travel.qunar.com/travelbook/list.htm?page={}&order=hot_heat"


for i in range(1,201):

    url=base_url.format(i)

    try:
        response=requests.get(url,headers=headers)

        response.encoding="utf-8"

        root=BeautifulSoup(response.text,"lxml")

        all_urls=root.find_all('li',attrs={'class':'list_item'})

        print("正在爬取第{}页".format(i))

        for each in all_urls:

            each_url=each.find('h2')['data-bookid']

            local_file.write(each_url+"\n")

        time.sleep(random.randint(3,5))

    except Exception as e:
        print(e)
