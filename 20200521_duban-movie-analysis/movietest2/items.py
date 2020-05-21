# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movietest2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 电影 id
    movie_id=scrapy.Field()

    # 电影名称
    movie_title=scrapy.Field()

    # tag
    movie_tag=scrapy.Field()

    # 电影评分
    movie_rate=scrapy.Field()

    # 导演
    movie_director=scrapy.Field()

    # 类型
    movie_types=scrapy.Field()

    # 制片国家
    movie_country=scrapy.Field()

    # 片长
    how_long=scrapy.Field()

    # 用户名
    user_name=scrapy.Field()

    # 评论内容
    content=scrapy.Field()

    # 发布时间
    release_time=scrapy.Field()

    # 用户链接
    user_link=scrapy.Field()

    # 用户id
    user_id=scrapy.Field()



