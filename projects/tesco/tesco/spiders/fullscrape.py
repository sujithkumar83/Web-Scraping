# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FullscrapeSpider(CrawlSpider):
    name = 'fullscrape'
    allowed_domains = ['https://www.tesco.com', 'tesco.com']
    start_urls = ['https://www.tesco.com/groceries']

    # Unlike basic template the callback method should have the parse item in quotes
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='navigation__nav-items']/li/div[@data-auto='menu-tree']/div/ul/li[@role='menuitem']/a"), callback='parse_supdept', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='navigation__nav-items']/li/div[@data-auto='menu-tree']/div/ul/li[@role='menuitem']/a"), callback='parse_dept', follow=True),
    )

    def parse_supdept(self, response):
        print(response.url)
    def parse_dept(self, response):
        print(response.url)
