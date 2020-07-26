# -*- coding: utf-8 -*-
import scrapy


class TescoSpider(scrapy.Spider):
    name = 'tesco'
    allowed_domains = ['https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo']
    start_urls = ['http://https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo/']

    def parse(self, response):
        pass
