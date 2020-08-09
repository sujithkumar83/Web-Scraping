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
        self.connection=sqlite3.connect("morrisons.db")
        self.c= self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE products(
                
                client TEXT,
                time TEXT,
                category TEXT,
                id TEXT,
                prod_name TEXT,
                morrisons_new_flag TEXT,
                morrisons_Qty TEXT,
                morrisons_old_price TEXT,
                morrisons_discounted_price TEXT,
                morrisons_offer_desc TEXT,
                morrisons_url TEXT,
                morrisons_rating TEXT,
                morrisons_unit_price TEXT,
                morrisons_availability TEXT,
                morrisons_prod_name TEXT
                
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
                morrisons_new_flag,
                morrisons_Qty,
                morrisons_old_price,
                morrisons_discounted_price,
                morrisons_offer_desc,
                morrisons_url,
                morrisons_rating,
                morrisons_unit_price,
                morrisons_availability,
                morrisons_prod_name) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
                item.get('client'),
                item.get('time'),
                item.get('category'),
                item.get('id'),
                item.get('prod_name'),
                item.get('morrisons_new_flag'),
                item.get('morrisons_Qty'),
                item.get('morrisons_old_price'),
                item.get('morrisons_discounted_price'),
                item.get('morrisons_offer_desc'),
                item.get('morrisons_url'),
                item.get('morrisons_rating'),
                item.get('morrisons_unit_price'),
                item.get('morrisons_availability'),
                item.get('morrisons_prod_name')
        ))
        self.connection.commit()
        return item

class ImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'imagename': item.get('image_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        return 'full/%s.jpg' % (request.meta['imagename'])