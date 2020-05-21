# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from movietest2.items import Movietest2Item

import json
import re
import time
import random


class Movie2Spider(CrawlSpider):
    name = 'movie2'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/search_tags?type=movie&tag=%E7%83%AD%E9%97%A8&source=']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self,response):

        tags=json.loads(response.text)['tags']

        base_url="https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=recommend&page_limit=20&page_start={}"

        for tag in tags:

            for i in range(100,161,20):

                items={
                    'tag':tag
                }

                url=base_url.format(tag,i)

                yield scrapy.Request(url=url,callback=self.parse_data,meta={"item":items},dont_filter=True)


    def parse_data(self,response):

        items=response.meta['item']

        data = json.loads(response.text)
        data = data['subjects']

        for i in data:

            items['title']=i['title']
            items['id']=int(i['id'])
            items['rate']=float(i['rate'])

            movie_url=i['url']

            yield scrapy.Request(url=movie_url,callback=self.parse_movie,meta={'item':items},dont_filter=True)

    def parse_movie(self,response):

        items=response.meta['item']

        #types=response.xpath('//span[@property="v:genre"]/text()').get()
        #types=str(types)
        pattern1 = re.compile(r'v:genre">(.*?)</span>')
        types = pattern1.findall(response.text)

        #country=response.xpath('//*[@id="info"]/text()[3]').get()
        pattern2 = re.compile(r'class="pl">制片国家/地区:</span>(.*?)<br/>')
        country = pattern2.findall(response.text)[0]

        #how_long=response.xpath('//*[@id="info"]/span[15]').get()
        pattern3 = re.compile(r'runtime" content="(.*?)">(.*?)</span')
        how_long = pattern3.findall(response.text)[0][1]

        #synopsis=response.xpath('//*[@id="link-report"]/span[1]/text()').get()
        pattern4 = re.compile(r'directedBy">(.*?)</a>')
        director = pattern4.findall(response.text)[0]


        items['types']=types
        items['director']=director
        items['country']=country
        items['how_long']=how_long

        for i in range(0,41,20):

            comment_url=response.url+"comments?start="+str(i)

            yield scrapy.Request(url=comment_url,callback=self.parse_comment,meta={'item':items},dont_filter=True)


    def parse_comment(self,response):

        items=response.meta['item']

        id=items['id']
        title=items['title']
        tag=items['tag']
        rate=items['rate']
        director=items['director']
        types=items['types']
        country=items['country']
        how_long=items['how_long']



        user_data = response.xpath('//div[@class="comment"]')

        for data in user_data:
            user_name = data.xpath('h3/span[2]/a/text()').get()
            content = data.xpath('p/span/text()').get()
            release_time = data.xpath('h3/span[2]/span[3]/@title').get()
            user_link = data.xpath('h3/span[2]/a/@href').get()
            user_id=user_link.split('/')[-2]

            item = Movietest2Item(
                user_id=user_id,
                user_name=user_name,
                content=content,
                user_link=user_link,
                movie_id=id,
                movie_title=title,
                movie_tag=tag,
                movie_rate=rate,
                movie_director=director,
                movie_types=types,
                movie_country=country,
                how_long=how_long,
                release_time=release_time
            )

            yield item

        time.sleep(random.randint(3,6))
