# -*- coding: utf-8 -*-
import scrapy


class AsdaShampooSpider(scrapy.Spider):
    name = 'asda_shampoo'
    allowed_domains = ['https://groceries.asda.com']
    start_urls = ['https://groceries.asda.com/shelf/health-beauty/hair-care/shampoo-conditioner/shampoo/103730']

    def parse(self, response):
        for product in response.xpath("//div[@class=' co-product-list']/ul[@class=' co-product-list__main-cntr']/li/div[@class='co-product']"):
            yield {
                #'id': product.xpath(".//div[@class='co-product']/div[@class='productNameAndPromotions']/div/@barcode").get(),
                #'prod_name': product.xpath(".//div/div[@class='co-item__title-container']/h3/a/text()").getall(),
                 'qty': product.xpath(".//div[@class='co-item__volume-container co-item__items']/span/text()").getall()
                # 'discounted_price': product.xpath(".//strong[@class='co-product__price']/text()").get(),
                # 'offer_desc': product.xpath(".//span[@class='co-product__promo-text')]/text()").get(),     
                # 'url': response.urljoin(product.xpath(".//div[@class='co-item__title-container']/h3/a/@href").get()),
                # 'rating': product.xpath(".//div[@class='rating-stars']/@aria-label").get(),           
                # 'unit_price': product.xpath(".//span[@class='co-product__price-per-uom')]/text()").get(),
                # 'orig_price': product.xpath(".//span[@class='co-product__was-price']/text()").get()

                    }

