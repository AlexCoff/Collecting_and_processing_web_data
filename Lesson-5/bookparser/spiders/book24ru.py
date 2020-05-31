# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['http://book24.ru/']
    def __init__(self, book_name):
        self.start_urls = [f'https://book24.ru/search/?q={book_name}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='catalog-pagination__item _text js-pagination-catalog-item']/@href").extract_first()
        book_links = response.xpath("//a[@class='book__image-link js-item-element ddl_product_link']/@href").extract()
        for book in book_links:
            yield response.follow(book, callback=self.book_parser)
        yield response.follow(next_page, callback=self.parse)


    def book_parser(self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//div[@class='item-tab__chars-list']/div[1]//a[contains(@class,'item')]/text()").extract()
        main_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        sel_price = response.xpath("//div[@class='item-actions__prices']/div/b/text()").extract_first()
        rate = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        yield BookparserItem(name=name,url=url,author=author,main_price=main_price,sel_price=sel_price,rate=rate)