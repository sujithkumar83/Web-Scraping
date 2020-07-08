# -*- coding: utf-8 -*-
import scrapy


class MorrisonHaircareSpider(scrapy.Spider):
    name = 'morrison_haircare'
    allowed_domains = ['https://groceries.morrisons.com']
    start_urls = ['https://groceries.morrisons.com/browse/toiletries-beauty-102838/hair-care-103040/shampoo-conditioner-181078']

    def parse(self, response):
        for product in response.xpath("//ul[@class='fops fops-regular fops-shelf']/li/div[@class='fop-item fop-item-offer']"):
            yield {
                'id': product.xpath(".//div[@data-sku]"),
                'prod_name': product.xpath(".//h4[@class='fop-title']/@title").get(),
                'Qty': product.xpath(".//div[@class='fop-description']/span[@class='fop-catch-weight']/text()").get(),
                'discounted_price': product.xpath(".//div[@class='price-group-wrapper']/span[@class='fop-price']/text()").get(),
                'offer_desc': product.xpath(".//a[@class='fop-row-promo promotion-offer']/span/text()").get(),     
                'url': response.urljoin(product.xpath(".//div[@class='fop-contentWrapper']/a/@href").get()),
                'rating': product.xpath(".//div[@class='review-wrapper']/span[@class='fop-rating']/span[@class='fop-rating-inner']/@title").get(),           
                'unit_price': product.xpath(".//div[@class='price-group-wrapper']/span[@class='fop-unit-price']/text()").get()

                    }