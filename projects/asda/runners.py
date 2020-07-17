import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from asda.spiders.asda_shampoo import AsdaShampooSpider

process= CrawlerProcess(settings=get_project_settings())
process.crawl(AsdaShampooSpider)
process.start()

