# -*- coding: utf-8 -*-
import scrapy


class SainsburysHaircareSpider(scrapy.Spider):
    name = 'sainsburys_haircare'
    allowed_domains = ['https://www.sainsburys.co.uk']
    start_urls = ['https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productLister gridView']/li[@class='gridItem']/div[contains(@class,'product')]"):
            yield {
                'id': product.xpath(".//div[contains(@class,'productInfo')]/div[@class='productNameAndPromotions']/div/@barcode").getall(),
                'prod_name': product.xpath(".//div[contains(@class,'productInfo')]/div[@class='productNameAndPromotions']/h3/a/text()[1]").getall(),
                'discounted_price': product.xpath(".//div[contains(@class,'addToTrolleytabBox')]/div/div/div/div[@class='pricing']/p[@class='pricePerUnit']/text()[1]").getall(),
                'offer_desc': product.xpath(".//div[contains(@class,'productInfo')]/div[@class='productNameAndPromotions']/div[@class='promotion']/p/a/text()").getall(),     
                'url': product.xpath(".//div[contains(@class,'productInfo')]/div[@class='productNameAndPromotions']/h3/a/@href").getall(),
                'rating': product.xpath(".//div[contains(@class,'addToTrolleytabBox')]/div/div/div/div[@class='reviews']/a/img/@alt").getall(),           
                'unit_price': product.xpath(".//div[contains(@class,'addToTrolleytabBox')]/div/div/div/div[@class='pricing']/p[@class='pricePerMeasure']/text()[1]").getall(),
                'unit_qty': product.xpath(".//div[contains(@class,'addToTrolleytabBox')]/div/div/div/div[@class='pricing']/p[@class='pricePerMeasure']/text()[2]").getall()

                    }
