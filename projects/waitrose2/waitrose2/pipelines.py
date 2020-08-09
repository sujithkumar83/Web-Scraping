# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from scrapy.pipelines.images import ImagesPipeline
import logging
import sqlite3
import scrapy
from scrapy import Request 

class SQLlitePipeline(object):
    
    
    # @classmethod
    # def from_crawler(cls,crawler):
    # logging.warning(crawler.settings.get('MONGO_URI'))
    
    def open_spider(self, spider):
        self.connection=sqlite3.connect("waitrose.db")
        self.c= self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE products(
                
                client TEXT,
                time TEXT,
                category TEXT,
                id TEXT,
                prod_name TEXT,
                waitrose_qty TEXT,
                waitrose_discounted_price TEXT,
                waitrose_offer_desc TEXT,
                waitrose_url TEXT,
                waitrose_rating TEXT,
                waitrose_unit_price TEXT,
                waitrose_new_flag TEXT,
                waitrose_prod_name TEXT
                
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
                prod_name,
                waitrose_qty,
                waitrose_discounted_price,
                waitrose_offer_desc,
                waitrose_url,
                waitrose_rating,
                waitrose_unit_price,
                waitrose_new_flag,
                waitrose_prod_name
                ) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
                item.get('client'),
                item.get('time'),
                item.get('category'),
                item.get('id'),
                item.get('prod_name'),
                item.get('waitrose_qty'),
                item.get('waitrose_discounted_price'),
                item.get('waitrose_offer_desc'),
                item.get('waitrose_url'),
                item.get('waitrose_rating'),
                item.get('waitrose_unit_price'),
                item.get('waitrose_new_flag'),
                item.get('waitrose_prod_name')

        ))
        self.connection.commit()
        return item

# class ImageDownloaderPipeline(ImagesPipeline):

#     def get_media_requests(self, item, info):
#         return [Request(x, meta={'imagename': item.get('image_name')}) for x in item.get(self.images_urls_field, [])]

#     def file_path(self, request, response=None, info=None):
#         url = request.url
#         return 'full/%s.jpg' % (request.meta['imagename'])