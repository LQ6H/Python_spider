#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

import jieba
from collections import Counter
import pyecharts.options as opts
from pyecharts.charts import WordCloud


def get_text():

    f=open("comments.txt",encoding="utf-8")

    lines=f.read()

    text=lines.split("\n\n")

    return "".join(text)



def split_word(text):

    word_list=list(jieba.cut(text))

    with open("停用词库.txt") as f:
        meaningless_word=f.read().splitlines()

    result=[]

    for i in word_list:

        if i not in meaningless_word:
            result.append(i.replace(" ",""))

    return result

def word_counter(words):

    words_counter=Counter(words)

    words_list=words_counter.most_common(2000)

    return words_list


def word_cloud(data):
    (
        WordCloud()
            .add(
            series_name="热点分析",
            data_pair=data,
            word_gap=5,
            word_size_range=[10,80],
            shape="cursive",
            mask_image="书.jpg"
        ).set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析",title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .render("basic.html")
    )


def main():

    text=get_text()

    words=split_word(text)

    data=word_counter(words)

    word_cloud(data)

if __name__ == '__main__':

    main()