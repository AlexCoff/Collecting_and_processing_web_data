# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from buildmparser.items import BuildmparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru','res.cloudinary.com']
    def __init__(self, search_item):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search_item}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        materials_links = response.xpath("//a[@class='link-wrapper']/@href").extract()
        for material in materials_links:
            yield response.follow(material, callback=self.materials_parser)
        yield response.follow(next_page, callback=self.parse)

    def materials_parser(self, response: HtmlResponse):
        loader = ItemLoader(item=BuildmparserItem(),response=response)
        loader.add_value('url',response.url)
        loader.add_xpath('name',"//h1/text()")
        loader.add_xpath('photo_list',"//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('avalability',"//uc-pdp-card-ga-enriched[@class='card-data']//uc-stock-availability/text()")
        loader.add_xpath('params_list',"//div[@class='def-list__group']")
        #loader.add_xpath('photo_list',"//picture[contains(@id,'picture-box-id-generated')]/source[1]/@data-origin")
        #loader.add_xpath('photo_list',"//img[@slot='thumbs']/@src")
        yield loader.load_item()
        #yield BuildmparserItem(name=name,url=url,avalability=avalability,params_list=params_list,photo_list=photo_list)
