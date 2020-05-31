# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']

    def __init__(self, book_name):
        self.start_urls = [f'https://www.labirint.ru/search/{book_name}/']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        book_links = response.xpath("//a[@class='cover']/@href").extract()
        for book in book_links:
            yield response.follow(book, callback=self.book_parser)
        yield response.follow(next_page, callback=self.parse)


    def book_parser(self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//a[@data-event-label='author']/text()").extract()
        main_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        sel_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        yield BookparserItem(name=name,url=url,author=author,main_price=main_price,sel_price=sel_price,rate=rate)
