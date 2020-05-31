# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class BuildmparserPipeline:
    def __init__(self):
        client = MongoClient('10.0.0.85',27017)
        self.mongo_base = client['materials_db']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['_id'] = hash(item['url'])
        collection.update_one({'_id':item['_id']},{'$set':item},upsert=True)
        return item

class LeroyPhotoPipelines(ImagesPipeline):
    def get_media_requests(self,item,info):
        if item['photo_list']:
            for img in item['photo_list']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
    #def item_completed(self,results,item,info):
    #    if results:
    #        item['photo_list'] = [itm[1] for itm in results if itm[0]]
    #    return item
    def item_completed(self, results, item, info):
        if results:
            item['photo_list'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        img_name = str(hash(request.meta['image_name']))+'.jpg'
        return img_name