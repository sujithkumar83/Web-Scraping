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
        self.connection=sqlite3.connect("asda.db")
        self.c= self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE products(
                
                client TEXT,
                time TEXT,
                category TEXT,
                id TEXT,
                prod_name TEXT,
                asda_qty TEXT,
                asda_discounted_price TEXT,
                asda_offer_desc TEXT,
                asda_url TEXT,
                asda_rating TEXT,
                asda_unit_price TEXT,
                asda_orig_price TEXT,
                asda_prod_name TEXT
                
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
                asda_qty,
                asda_discounted_price,
                asda_offer_desc,
                asda_url,
                asda_rating,
                asda_unit_price,
                asda_orig_price,
                asda_prod_name
                ) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
                item.get('client'),
                item.get('time'),
                item.get('category'),
                item.get('id'),
                item.get('prod_name'),
                item.get('asda_qty'),
                item.get('asda_discounted_price'),
                item.get('asda_offer_desc'),
                item.get('asda_url'),
                item.get('asda_rating'),
                item.get('asda_unit_price'),
                item.get('asda_orig_price'),
                item.get('asda_prod_name')

        ))
        self.connection.commit()
        return item

class ImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'imagename': item.get('image_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        return 'full/%s.jpg' % (request.meta['imagename'])