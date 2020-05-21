# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json

class Movietest2Pipeline(object):
    collection_name="test"

    def __init__(self,mongo_uri,mongo_db):

        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE','Movie')
        )


    def open_spider(self,spider):

        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]


    def close_spider(self,spider):

        self.client.close()


    def process_item(self, item, spider):

        self.db[self.collection_name].insert(dict(item))
        return item


class Movietest2FilePipeline(object):

    def open_spider(self,spider):
        #self.file=open("review_final.json","a",encoding="utf-8")
        self.file = open("test.json", "a", encoding="utf-8")

    def process_item(self,item,spider):

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"

        self.file.write(line)

        return item

    def close_spider(self,spider):

        self.file.close()


"""
class Movietest2CsvPipeline(object):

    def __init__(self):

        self.f=open('review.csv','a',encoding="utf-8")

        self.exportre=CsvItemExporter(
            self.f,
            include_headers_line=True,
            encoding='utf-8'
        )

    def open_spider(self,spider):

        pass

    def process_item(self,item,spider):

        self.exportre.export_item(item)

        return item

    def close_spider(self,spider):

        self.f.close()


"""




