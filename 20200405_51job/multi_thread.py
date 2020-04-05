#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
import threading
from lxml import etree
import json
import time
import random
import re
import pandas as pd
from queue import Queue

# 采集网页页码队列是否为空的信号
CRAWL_EXIT = False


class ThreadCrawl(threading.Thread):

    def __init__(self, threadName, pageQueue, dataQueue):
        threading.Thread.__init__(self)

        # 线程名
        self.threadName = threadName

        # 页码队列
        self.pageQueue = pageQueue

        # 数据队列
        self.dataQueue = dataQueue

        #self.base_url = "******"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Cookie": "******"
        }

    def run(self):

        print("启动：" + self.threadName)

        while not CRAWL_EXIT:

            try:
                # 从 pageQueue 中取出一个页码数字，先进先出
                # 可选参数block 默认值为True
                # 如果队列为空 block为True 会进入阻塞状态 直到队列有新的数据
                # 如果队列为空 block为False 会返回一个Queue.empty()异常

                url = self.pageQueue.get(False)

                response = requests.get(url, headers=self.headers)
                response.encoding = "gbk"
                html = response.text

                self.dataQueue.put(html)
            except Exception as e:
                print(e)

        print("结束：" + self.threadName)


# 网页源代码队列是否为空的信号
PARSE_EXIT = False


class ThreadParse(threading.Thread):

    def __init__(self, threadName, dataQueue, localFile, lock):

        super(ThreadParse, self).__init__()

        # 线程名
        self.threadName = threadName

        # 数据队列
        self.dataQueue = dataQueue

        # 保存解析后数据的文件名
        self.localFile = localFile

        # 互斥锁
        self.lock = lock

    def run(self):

        print("启动：" + self.threadName)

        while not PARSE_EXIT:

            try:

                html = self.dataQueue.get(False)
                self.parse1(html)
            except Exception as e:
                print(e)

        print("结束：" + self.threadName)

    def parse1(self, html):

        root = etree.HTML(html)

        try:

            items={}

            # 1.岗位名称
            items['job_name'] = root.xpath('string(//div[@class="cn"]/h1/@title)')

            # 2.公司名称
            items['company_name'] = root.xpath('string(//div[@class="cn"]/p/a/@title)')

            random_all = root.xpath('//div[@class="cn"]//p[@class="msg ltype"]/text()')
            items['random_all'] = [i.replace('\xa0', '').strip() for i in random_all]

            # 3.工作地点
            items['address'] = random_all[0]

            # 4.工资
            salary_mid = root.xpath('string(//div[@class="cn"]/strong/text())')
            items['salary'] = salary_mid if salary_mid else '-'

            # 5.发布时间
            release = "".join(random_all)
            items['release_time'] = re.findall('\d+-\d+', release)[-1]

            # 6.混合数据(经验，学历等)


            # 7.岗位描述信息
            items['job_drscribe'] = root.xpath('string(//div[@class="bmsg job_msg inbox"])').replace("\xa0", "").replace("\r\n",
                                                                                                            "").strip()

            # 8.公司类型
            items['company_type'] = root.xpath('string(//div[@class="com_tag"]/p[1]/@title)')

            # 9.公司规模
            items['company_size'] = root.xpath('string(//div[@class="com_tag"]/p[2]/@title)')

            # 10.所属行业
            items['industry'] = root.xpath('string(//div[@class="com_tag"]/p[3]/@title)')


            with self.lock:
                self.localFile.write(json.dumps(items, ensure_ascii=False) + "\n")
        except Exception as e:
            print(e)


    def parse2(self, html):

        root = etree.HTML(html)

        # 1.标题
        title = root.xpath('//div[@class="post-head"]/h1/a/text()')
        title = [i.split("_")[0] for i in title]

        # 2.内容
        content = root.xpath('//div[@class="post-content"]/p/text()')

        # 3.热度
        hot = root.xpath('//div[@class="post-meta"]/time[2]/text()')
        hot = [i.replace("°C", "") for i in hot]

        # 4.赞
        zan = root.xpath('//div[@class="post-meta"]/time[3]/a/span/text()')

        # 5.发布时间
        release_time = root.xpath('//div[@class="post-meta"]/time[1]/text()')

        df = pd.DataFrame()
        df['title'] = title
        df['content'] = content
        df['hot'] = hot
        df['zhan'] = zan
        df['date'] = release_time

        try:
            with self.lock:
                df.to_csv("job_info2_2.csv", mode="a+", header=None, index=None, encoding="utf-8")
        except Exception as e:
            print(e)


def main():

    url_list = []
    with open('urls.txt', 'r', encoding="utf-8") as f:
        for i in f.readlines():
            i = i.strip()
            url_list.append(i)


    pageQueue = Queue()

    for i in url_list:
        pageQueue.put(i)

    dataQueue = Queue()

    localFile = open("job_info2_1.json", "a", encoding="utf-8")

    lock = threading.Lock()

    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]

    threadCrawls = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadCrawls.append(thread)

    parseList = ["解析线程1号", "解析线程2号", "解析线程3号"]

    threadParses = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, localFile, lock)
        thread.start()
        threadParses.append(thread)

    while not pageQueue.empty():
        pass

    global CRAWL_EXIT
    CRAWL_EXIT = True

    print("pageQueue为空")

    for thread in threadCrawls:
        thread.join()

    while not dataQueue.empty():
        pass

    print("dataQueue为空")

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadParses:
        thread.join()

    with lock:
        localFile.close()


if __name__ == "__main__":

    startTime=time.time()

    main()

    print(time.time()-startTime)