# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import logging
import sqlite3
import scrapy
from scrapy import Request  

class SQLlitePipeline(object):
    
    
    # @classmethod
    # def from_crawler(cls,crawler):
    # logging.warning(crawler.settings.get('MONGO_URI'))
    
    def open_spider(self, spider):
        self.connection=sqlite3.connect("sainsburys.db")
        self.c= self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE products(
                
                client TEXT,
                time TEXT,
                category TEXT,
                id TEXT,
                sainsburys_prod_name TEXT,
                sainsburys_discounted_price TEXT,
                sainsburys_offer_desc TEXT,
                sainsburys_url TEXT,
                sainsburys_rating TEXT,
                sainsburys_unit_price TEXT,
                sainsburys_availability TEXT

                
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
    
    def close_spider(self, spider):
        self.connection.close()
    
    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO products (
                client,
                time,
                category,
                id,
                sainsburys_prod_name,
                sainsburys_discounted_price,
                sainsburys_offer_desc,
                sainsburys_url,
                sainsburys_rating,
                sainsburys_unit_price,
                sainsburys_availability
                ) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ''', (
                item.get('client'),
                item.get('time'),
                item.get('category'),
                item.get('id'),
                item.get('sainsburys_prod_name'),
                item.get('sainsburys_discounted_price'),
                item.get('sainsburys_offer_desc'),
                item.get('sainsburys_url'),
                item.get('sainsburys_rating'),
                item.get('sainsburys_unit_price'),
                item.get('sainsburys_availability')

        ))
        self.connection.commit()
        return item



class ImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'imagename': item.get('image_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        return 'full/%s.jpg' % (request.meta['imagename'])