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
        self.connection=sqlite3.connect("tesco.db")
        self.c= self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE products(
                
                client TEXT,
                time TEXT,
                category TEXT,
                tesco_prod_name TEXT,
                tesco_new_flag TEXT,
                tesco_discounted_price TEXT,
                tesco_offer_desc TEXT,
                tesco_url TEXT,
                tesco_unit_price TEXT,
                tesco_unit_weight TEXT

                
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
                tesco_prod_name,
                tesco_new_flag,
                tesco_discounted_price,
                tesco_offer_desc,
                tesco_url,
                tesco_unit_price,
                tesco_unit_weight

                ) 
                VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (
                item.get('client'),
                item.get('time'),
                item.get('category'),
                item.get('tesco_prod_name'),
                item.get('tesco_new_flag'),
                item.get('tesco_discounted_price'),
                item.get('tesco_offer_desc'),
                item.get('tesco_url'),
                item.get('tesco_unit_price'),
                item.get('tesco_unit_weight')


        ))
        self.connection.commit()
        return item

class ImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'imagename': item.get('image_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        return 'full/%s.jpg' % (request.meta['imagename'])