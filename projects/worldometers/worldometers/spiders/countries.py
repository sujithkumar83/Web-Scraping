# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info/world-population/population-by-country/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country//']

    def parse(self, response):
        pass
