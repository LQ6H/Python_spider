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

base_url="http://pic.netbian.com/4kmeinv/index_{}.html"

folder_path="./photoes/"

count=1

def spider(urls):

    global count

    for index, item in enumerate(urls):
        response = requests.get(item)

        img_name = folder_path + str(count) + ".jpg"

        with open(img_name, "wb") as f:
            f.write(response.content)
            f.flush()

        f.close()

        print("第%d张图片下载完成" % (count))

        time.sleep(random.randint(3,5))

        count+=1


def main():

    picture_path="./photoes/"

    if os.path.exists(picture_path)== False:
        os.makedirs(picture_path)

    for page in range(1,196):

        url="http://pic.netbian.com/4kmeinv/index.html"

        if page!=1:
            url=base_url.format(page)

        response=requests.get(url,headers=headers)
        response.encoding="gbk"
        html=response.text
        root=etree.HTML(html)

        imgs_link = root.xpath('//ul[@class="clearfix"]/li/a/img/@src')

        urls = []

        for i in imgs_link:
            urls.append("http://pic.netbian.com" + i)

        spider(urls)

if __name__=="__main__":

    main()
