#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

from flask import Flask,render_template
import os


app = Flask(__name__)

@app.route('/test')
def index():
    filepath_list = os.listdir('./static')
    path_list = []
    for path in filepath_list:
        path = '/static/'+path
        path_list.append(path)

    print(path_list)

    return render_template('./main.html',path_list=path_list)

if __name__ == "__main__":
    app.run(debug=True)










