#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import requests
import re
import time

for i in range(0,341,20):

    # 閫氳繃娴忚鍣ㄦ鏌ワ紝寰楀埌鏁版嵁鐨刄RL鏉ユ簮閾炬帴
    url='https://movie.douban.com/subject/26774119/comments?start={}&limit=20&sort=new_score&status=P'.format(i)

    # 鐮磋В闃茬埇铏紝甯︿笂璇锋眰澶�
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer':'https://www.douban.com/gallery/topic/125573/?from=gallery_trend&sort=hot'
    }

    # 鍙戦€佽姹傦紝鑾峰彇鍝嶅簲
    response=requests.get(url,headers=headers).text

    comments = re.findall('short">(.*?)</span>', response)

    # 瑙ｆ瀽鏁版嵁锛岃幏寰楃煭璇�
    # 淇濆瓨鍒版湰鍦�
    for comment in comments:
        with open('comments.txt','a',encoding='utf-8') as f:
            f.write(comment+'\n\n')

    time.sleep(2)
