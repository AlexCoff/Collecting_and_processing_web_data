# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from buildmparser.items import BuildmparserItem

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
        url = response.url
        name = response.xpath("//h1/text()").extract_first()
        avalability = response.xpath("//uc-pdp-card-ga-enriched[@class='card-data']//uc-stock-availability/text()").extract()
        params_list = response.xpath("//div[@class='def-list__group']").extract()
        photo_list = response.xpath("//picture[contains(@id,'picture-box-id-generated')]/source[1]/@data-origin")
        yield BuildmparserItem(name=name,url=url,avalability=avalability,params_list=params_list,photo_list=photo_list)
