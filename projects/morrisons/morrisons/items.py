# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import os

def remove_extension(value):

    return os.path.splitext(value)[0]
class MorrisonsItem(scrapy.Item):
    
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name=scrapy.Field(
        input_processor = MapCompose(remove_extension),
        Output_processor = TakeFirst()
    )
