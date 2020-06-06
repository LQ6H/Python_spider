#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import requests
from baidu_api import baidu
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}


def parse(url):

    response = requests.get(url,headers=headers)

    response.encoding = 'utf-8'

    html = response.text

    root = etree.HTML(html)

    parse_html(root)


def parse_html(root):

    article_list = root.xpath('/html/body/section/div/div/main/article')

    for article in article_list:

        title = article.xpath('./div[1]/h1/a/text()')[0]
        content = article.xpath('./div[2]/pre/code/text()')[0]

        baidu(title,content)




def main():
    base_url = 'https://duanziwang.com/page/{}/'

    for i in range(2,5):
        url = base_url.format(i)

        parse(url)


if __name__=="__main__":

    main()