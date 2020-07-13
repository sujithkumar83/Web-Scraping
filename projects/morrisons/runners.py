import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from morrisons.spiders.morrison_haircare import MorrisonHaircareSpider

process= CrawlerProcess(settings=get_project_settings())
process.crawl(MorrisonHaircareSpider)
process.start()

