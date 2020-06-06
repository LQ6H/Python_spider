#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import os

from aip import AipSpeech

APP_ID = '20257660'
API_KEY = 'QmnUG6DxYf0DFw1Fjx9IeLqk'
SECRET_KEY = '******'

client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

def baidu(title,content):

    result = client.synthesis(content,'zh',1,{'vol':5})

    filename = os.path.join('./static/',title+'.mp3')

    if not isinstance(result,dict):
        with open(filename,'wb') as f:
            f.write(result)

        print(filename + "已存入")
