# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class BuildmparserPipeline:
    def __init__(self):
        client = MongoClient('10.0.0.85',27017)
        self.mongo_base = client['materials_db']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['_id'] = hash(item['url'])
        collection.update_one({'_id':item['_id']},{'$set':item},upsert=True)
        return item
