# -*- coding: utf-8 -*-
import scrapy


class WaitroseShampooSpider(scrapy.Spider):
    name = 'waitrose_shampoo'
    allowed_domains = ['https://www.waitrose.com/']
    start_urls = ['https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo']

    

    def parse(self, response):
        for product in response.xpath("//main[@class='appMain___2G0oc']/div/div/div/div[contains(@class,'row')]/article"):
            yield {
                'id': product.xpath(".//@id").get(),
                'prod_name': product.xpath(".//@data-product-name").get(),
                'Qty': product.xpath(".//div/section/header/a/span/text()").get(),
                'discounted_price': product.xpath(".//div/section/div/span[@data-test='product-pod-price']/span/text()").get(),
                'offer_desc': product.xpath(".//div/section/header/div/div/div/a/p/span/text()").get(),     
                'url': response.urljoin(product.xpath(".//div/sectio/header/a/@href").get()),
                'rating': product.xpath(".//div/section/div/p/a/span/span/span/text()").get(),           
                'unit_price': product.xpath(".//div/section/div/span[@class='pricePerUnit___1gifh priceInfo___1J8aK']/text()").get()

                    }
