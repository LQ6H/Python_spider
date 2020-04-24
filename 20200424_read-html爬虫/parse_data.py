#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H


import pandas as pd


url='https://www.kuaidaili.com/free'
#url='https://www.xicidaili.com'
#url='http://www.goubanjia.com/'

df=pd.read_html(url,encoding="utf-8")[0]

#print(df)

df.to_csv('free_ip.csv',mode="a",encoding="utf-8",header=1,index=0)
