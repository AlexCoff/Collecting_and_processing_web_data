# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose,TakeFirst
from lxml import html
import re
import scrapy

# Create dict of parameters
def params_parser(value):
    params = {}
    dom = html.fromstring(value)
    params['pname'] = re.sub(r'\s\s+',' ',dom.xpath(".//dt/text()")[0])
    params['value'] = re.sub(r'\s\s+',' ',dom.xpath(".//dd/text()")[0])
    return params


class BuildmparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photo_list = scrapy.Field(input_processor=MapCompose())
    avalability = scrapy.Field(output_processor=TakeFirst())
    params_list = scrapy.Field(input_processor=MapCompose(params_parser))
    #params_list = scrapy.Field()
    print(1)
