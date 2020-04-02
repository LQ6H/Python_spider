#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
import time
import csv
import random
from lxml import etree


headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "cookie":"******",
    "referer":"https://travel.qunar.com/travelbook/list.htm?page=1&order=hot_heat"
}


url_list=[]
with open('urls.txt','r',encoding="utf-8") as f:
    for i in f.readlines():
        i=i.strip()
        url_list.append(i)


the_url_list=[]
for i in range(len(url_list)):
    url='http://travel.qunar.com/youji/'+str(url_list[i])
    the_url_list.append(url)

info_list = []

def spider():

    for i in range(len(the_url_list)):

        try:
            print("正在爬取第{}页".format(i+1))

            response=requests.get(the_url_list[i],headers=headers)

            response.encoding="utf-8"

            html=response.text

            root=etree.HTML(html)

            information=root.xpath('string(//p[@class="b_crumb_cont"])').strip().replace(' ','')

            info=information.split('>')

            if len(info) > 2:
                location = info[1].replace('\xa0', '').replace('旅游攻略', '')
                introduction = info[2].replace('\xa0', '')
            else:
                location = info[1].split("｜")[0].replace('\xa0', '')
                introduction = info[1].replace('\xa0', '')


            when = root.xpath('string(//li[@class="f_item when"]/p)').replace('出发日期', '').strip()

            howlong = root.xpath('string(//li[@class="f_item howlong"]/p)').replace('天数', '').replace('/', '').replace('天', '').strip()

            howmuch = root.xpath('string(//li[@class="f_item howmuch"]/p)').replace('人均费用', '').replace('/', '').replace('元','').strip()

            who = root.xpath('string(//li[@class="f_item who"])').replace('人物', '').replace('/', '').strip()

            play = root.xpath('string(//li[@class="f_item how"])').replace('玩法', '').replace('/', '').strip()

            Look = root.xpath('//span[@class="view_count"]/text()')[0]

            if when:
                When=when
            else:
                When = '-'
            if howlong:
                Howlong = howlong
            else:
                Howlong = '-'
            if howmuch:
                Howmuch = howmuch
            else:
                Howmuch= '-'
            if who:
                Who = who
            else:
                Who = '-'
            if play:
                Play = play
            else:
                Play = '-'


            info_list.append([location,introduction,When,Howlong,Howmuch,Who,Play,Look])
            # 设置爬虫时间
            time.sleep(random.randint(3, 5))

        except Exception as e:
            print(e)

    # 写入csv
    with open('travel2.csv', 'a', encoding='utf-8', newline='') as csvFile:
        csv.writer(csvFile).writerow(['地点', '短评', '出发时间', '天数', '人均费用', '人物', '玩法', '浏览量'])
        for rows in info_list:
            csv.writer(csvFile).writerow(rows)

    csvFile.close()

if __name__=="__main__":

    spider()