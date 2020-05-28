#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:LQ6H

import requests
import re
import json

headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}


def get_all_citys():

    url = 'https://uutool.cn/assets/js/tools/phone_generate.min.js?v=2'

    response = requests.get(url,headers=headers).text

    pattern1 = re.compile(r'areaArr:(.*?)segmentArr:')
    city = pattern1.findall(response)

    pattern2 = re.compile(r'segmentArr:(.*?),province:')
    segment = pattern2.findall(response)

    #citys = json.loads(city[-1])
    citys = city[-1]
    citys = citys.replace("id",'"id"')
    citys = citys.replace("name",'"name"')
    citys = json.loads(citys[:-1])
    segments = json.loads(segment[-1])

    return citys,segments




def generate_phones(segments,city_id,num):

    phone_num = num

    area = city_id

    segment = "134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 165, 172, 178, 182, 183, 184, 187, 188, 198,\
               130, 131, 132, 145, 155, 156, 166, 171, 175, 176, 185, 186,\
               133, 149, 153, 173, 177, 180, 181, 189, 199"
    
    data = {
        'phone_num':phone_num,
        'area':area,
        'segment':segment
    }

    try:

        response = requests.post('https://api.uukit.com/phone/generate_batch',headers=headers,data=data)

        phones = json.loads(response.text)["data"]["rows"]

        return phones
    except Exception as e:
        print(e)



def main():

    citys,segments =get_all_citys()

    num = int(input("请输入电话生成数目："))

    city_name = input("请输入手机归属地：")

    if city_name not in citys.keys():
        city_name = "北京"

    city_id = citys.get(city_name)

    id=[]
    for i in city_id:
        
        id.append(int(i["id"]))

    city_id = str(id)[1:-1]


    phones = generate_phones(segments,city_id,num)

    print(phones)


if __name__=="__main__":

   main()
