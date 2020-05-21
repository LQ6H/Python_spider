#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,WordCloud,Funnel,Line,Page
import pandas as pd
import json
import re
import csv
from collections import Counter
import jieba


def split_word(comment):
    word_list = list(jieba.cut(comment))

    with open("stop_words.txt", encoding="utf-8") as f:
        meaningless_word = f.read().splitlines()

    result = []

    for i in word_list:
        if i not in meaningless_word:
            result.append(i.replace(" ", ""))

    return result


def word_counter(words):
    words_counter = Counter(words)

    words_list = words_counter.most_common(100)

    return words_list


def save_data():
    datas = []

    with open("review_final.json", "r", encoding="utf-8") as f:

        for line in f.readlines():
            data = list(json.loads(line).values())
            datas.append(data)


    with open('review_final.csv', 'w', encoding='utf-8', newline='') as csvFile:
        csv.writer(csvFile).writerow(
            ['用户id', '用户名', '评论内容', '用户链接', '电影id', '电影title', '电影tag', '电影评分', '导演', '电影类型', '国家', '片长', '发布时间'])
        for rows in datas:
            csv.writer(csvFile).writerow(rows)

    f.close()

    df = pd.read_csv('review_final.csv', engine='python', encoding='utf-8')

    return df


def Pie1():
    x = list(df['用户id'].value_counts().index)[:10]
    y = list(df['用户名'].value_counts().head(10))

    data_pairs = [i for i in zip(x, y)]

    p1 = (
        Pie(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add(
            series_name="用户评论数量",
            data_pair=data_pairs
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="用户评论次数分析"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}：{c}"))
    )

    return p1


def Bar1():
    x = list(df['用户id'].value_counts().index)
    user = df[df['用户id'] == x[0]]
    user_type = user.loc[:, '电影类型']
    x = user_type.value_counts()

    res = "".join(list(x.index))

    pattern = re.compile(r'\w+')

    s = pattern.findall(res)

    res = Counter(s)

    x = []
    y = []

    for k, v in res.items():
        x.append(k)
        y.append(v)

    b1 = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add_xaxis(x)
            .add_yaxis("电影类型次数", y)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="用户观看电影类型分析"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )

    return b1


def Wordlound1():
    users = list(df['用户id'].value_counts().index)[:10]
    user_1 = df[df['用户id'] == users[0]]

    comment = "".join(user_1['评论内容'].to_list())
    pattern = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    comment = pattern.sub('', comment)

    words = split_word(comment)

    data = word_counter(words)

    w1 = (
        WordCloud()
            .add(
            series_name="用户评论词云",
            data_pair=data,
            word_size_range=[10, 120],
            shape="cursive"
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="用户评论", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )

    return w1


def Wordcloud2():
    comment1 = df[df["电影title"] == "阴曹使者"]
    comment1 = "".join(set(comment1['评论内容'].to_list()))

    pattern = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    comment1 = pattern.sub('', comment1)

    words = split_word(comment1)

    data = word_counter(words)

    w2 = (
        WordCloud()
            .add(
            series_name="电影评论客观词云",
            data_pair=data,
            word_size_range=[10, 120],
            shape="cursive"
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="电影评论客观词云", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )

    return w2


def Funnel1():
    movie_type = df['国家'].value_counts()
    x = list(movie_type.index)[:10]
    y = movie_type.to_list()[:10]

    data_pairs = [z for z in zip(x, y)]

    f1 = (
        Funnel()
            .add(
            series_name="",
            data_pair=data_pairs
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="电影国家比重"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="0%", pos_top="20%", orient="vertical")
        )
    )

    return f1

"""

def Line1():
    data = df.dropna()

    data.index = range(len(data))

    def Month(s):

        s = s.split('-')

        if s[1] == "01":
            return "一月"
        elif s[1] == "02":
            return "二月"
        elif s[1] == "03":
            return "三月"
        else:
            return "四月"

    data["电影月份"] = data["发布时间"].apply(Month)

    month = ["一月", "二月", "三月", "四月"]

    def average_rate():
        rate = []

        for i in month:
            month_res = data[data['电影月份'] == i]["电影评分"]
            result = float(sum(month_res.to_list()) / len(month_res.to_list()))

            result = float(str(result)[:4])

            rate.append(result)

        return rate

    rate = average_rate()

    l1 = (
        Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add_xaxis(month)
            .add_yaxis("电影评分", rate)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="评分")
        )
    )

    return l1


"""

def Pie2():
    types = df['电影tag'].value_counts()
    x = list(types.index)
    y = types.to_list()

    p2 = (
        Pie()
            .add("电影Tag",
                 [z for z in zip(x, y)]
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="电影类别统计"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}：{c}"))
    )

    return p2


def Pie3():
    types = df['电影tag'].value_counts()
    x = list(types.index)

    def average_rate():
        rate = []

        for i in x:
            month_res = df[df['电影tag'] == i]["电影评分"]
            result = float(sum(month_res.to_list()) / len(month_res.to_list()))

            result = float(str(result)[:4])

            rate.append(result)

        return rate

    rate = average_rate()

    p3 = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(x, rate)],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="电影类别平均评分"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="0%", pos_top="20%", orient="vertical"),
            toolbox_opts=opts.ToolboxOpts(is_show=True)
        )
    )

    return p3

def Bar2():
    types = df['电影tag'].value_counts()
    x = list(types.index)

    def average_rate():
        rate = []

        for i in x:
            month_res = df[df['电影tag'] == i]["电影评分"]
            result = float(sum(month_res.to_list()) / len(month_res.to_list()))

            result = float(str(result)[:4])

            rate.append(result)

        return rate

    rate = average_rate()

    b2 = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add_xaxis(x)
            .add_yaxis("电影Tag", rate)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="电影Tag评分"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )

    return b2

def Bar3():
    x = list(df["导演"].value_counts().index)[:10]

    def average_rate():
        rate = []

        for i in x:
            month_res = df[df['导演'] == i]["电影评分"]
            result = float(sum(month_res.to_list()) / len(month_res.to_list()))

            result = float(str(result)[:4])

            rate.append(result)

        return rate

    rate = average_rate()

    b3 = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add_xaxis(x)
            .add_yaxis("电影Tag", rate)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="电影导演评分"),
            # datazoom_opts=opts.DataZoomOpts(),
        )
    )

    return b3


def main():

    page=Page(layout=Page.DraggablePageLayout)

    page.add(
        Pie1(),
        Bar1(),
        Wordlound1(),
        Wordcloud2(),
        Funnel1(),
        Pie2(),
        Pie3(),
        Bar2(),
        Bar3(),
    )

    page.render("review_fun.html")


if __name__=="__main__":

    df=save_data()

    main()

















