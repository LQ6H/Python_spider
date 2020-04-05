#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
import threading
from lxml import etree
import json
import time
import random
import pandas as pd
from queue import Queue
import os
import re

url_list=[]
with open('urls.txt','r',encoding="utf-8") as f:
    for i in f.readlines():
        i=i.strip()
        url_list.append(i)


picture_path="./mul_photoes/"

if os.path.exists(picture_path)== False:
    os.makedirs(picture_path)


index=1

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

        #self.base_url = "https://duanziwang.com/category/%E7%BB%8F%E5%85%B8%E6%AE%B5%E5%AD%90/{}/"

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
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
                html = response.content

                self.dataQueue.put(html)
            except Exception as e:
                print(e)

        print("结束：" + self.threadName)


# 网页源代码队列是否为空的信号
PARSE_EXIT = False


class ThreadParse(threading.Thread):

    def __init__(self, threadName, dataQueue):

        super(ThreadParse, self).__init__()

        # 线程名
        self.threadName = threadName

        # 数据队列
        self.dataQueue = dataQueue

        # 保存解析后数据的文件名
        #self.localFile = localFile

        # 互斥锁
        #self.lock = lock

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
        global index

        try:
            img_name = picture_path + str(index) + ".jpg"

            index+=1

            with open(img_name, "wb") as f:
                f.write(html)
                f.flush()

            f.close()
        except Exception as e:
            print(e)




def main():


    pageQueue = Queue()

    for i in url_list:
        pageQueue.put(i)

    dataQueue = Queue()

    #localFile = open("duanzi2_1.json", "a", encoding="utf-8")

    #lock = threading.Lock()

    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]

    threadCrawls = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadCrawls.append(thread)

    parseList = ["解析线程1号", "解析线程2号", "解析线程3号"]

    threadParses = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue)
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

    #with lock:
    #    localFile.close()


if __name__ == "__main__":
    main()