#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import requests
from lxml import etree
import time
import random
import json


headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

local_file1=open("comments.json","a",encoding="utf-8")
local_file2=open('comments.txt',"a",encoding="utf-8")

def get_page():


    for i in range(500):

        base_url='https://movie.douban.com/subject/27010768/comments?start={}&limit=20&sort=new_score&status=P'.format(i)

        html=requests.get(base_url,headers=headers).text

        print("正在解析{}页".format(i+1))

        parse_html(html)

        time.sleep(random.random())



def parse_html(html):

    root=etree.HTML(html)

    name_list=root.xpath('//span[@class="comment-info"]/a/text()')
    comment_list=root.xpath('//span[@class="short"]/text()')
    time_list=root.xpath('//span[@class="comment-time "]/@title')

    #data=[]

    for i in range(len(name_list)):
        dic={}

        dic["name"]=name_list[i]
        dic["comment"]=comment_list[i]
        dic["time"]=time_list[i]

        #data.append(dic)

        local_file1.write(json.dumps(dic,ensure_ascii=False)+"\n")
        local_file2.write(comment_list[i]+"\n\n")



    #pd.DataFrame(data).to_csv('comments.csv', encoding='utf_8', index=False)


def main():
    get_page()


if __name__ == '__main__':

    main()

    local_file1.close()
    local_file2.close()
