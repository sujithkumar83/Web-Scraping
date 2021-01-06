# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class TescoShampooSpider2(scrapy.Spider):
    name = 'tesco_shampoo2'
    allowed_domains = ['https://www.tesco.com']
    #start_urls = ['https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo']

    
    def start_requests(self):
        yield scrapy.Request(url='https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo', callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            })
    client="Tesco"
    category="Shampoo"
    time = datetime.now()
    def parse(self, response):
        for product in response.xpath("//ul[@class='product-list grid']/li[contains(@class,'product-list--list-item')]"):
            yield {
                'client': self.client,
                'time': self.time,
                'category': self.category,
                #'id': product.xpath(".//@data-sku").get(),
                'tesco_prod_name': product.xpath(".//div[@class='product-details--wrapper']/div/h3/a/text()").get(),
                'tesco_new_flag': product.xpath(".//div[@class='product-widget--offer-flash']/p/strong/text()").get(),
                #'Qty': product.xpath(".//div[@class='fop-description']/span[@class='fop-catch-weight']/text()").get(),
                'tesco_discounted_price': product.xpath(".//div[@class='product-controls__wrapper']/form/div/div/div/div/div/span/span[@data-auto='price-value']/text()").get(),
                'tesco_offer_desc': product.xpath(".//div[@class='hidden-medium product-info-section-small']/div[@class='product-info-message-list']/div[@class='product-info-message']/p/text()").get(),
                'tesco_url': response.urljoin(product.xpath("//div[@class='product-details--wrapper']/div/h3/a/@href").get()),
                #'rating': product.xpath(".//div[@class='review-wrapper']/span[@class='fop-rating']/span[@class='fop-rating-inner']/@title").get(),
                'tesco_unit_price': product.xpath(".//div[@class='product-controls__wrapper']/form/div/div/div/span/span[@class='value']/text()").get(),
                'tesco_unit_weight': product.xpath(".//div[@class='product-controls__wrapper']/form/div/div/div/span[@class='weight']/text()").get()
                #'availability': product.xpath(".//div/a/span[@class='fop-mark-oos fop-image-corner']/text()").get()
            }
        next_url= response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get()
        if next_url:
            next_lnk= response.urljoin(response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get())
            yield scrapy.Request(url=next_lnk, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            },dont_filter=True)

