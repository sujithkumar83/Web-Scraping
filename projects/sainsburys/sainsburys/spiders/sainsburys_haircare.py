# -*- coding: utf-8 -*-
import scrapy


class SainsburysHaircareSpider(scrapy.Spider):
    name = 'sainsburys_haircare'
    allowed_domains = ['https://www.sainsburys.co.uk']
    start_urls = ['https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productLister gridView']/li[@class='gridItem']"):
            yield {
                'id': product.xpath(".//div/div/div/div[@class='FM_suitability_indicator']/@barcode").getall(),
                'prod_name': product.xpath(".//div/div/div/h3/a/text()[1]").getall(),
                'discounted_price': product.xpath(".//div/div/div/div/div/div/p[@class='pricePerUnit']/text()").getall(),
                'offer_desc': product.xpath(".//div/div/div/div/p/a/text()").getall(),     
                'url': product.xpath(".//div/div/div/h3/a/@href").getall(),
                'rating': product.xpath(".//div/div/div/div/div/div[@class='reviews']/a/img/@alt").getall(),           
                'unit_price': product.xpath(".//div/div/div/div/div/p[@class='pricePerMeasure']/text()[1]").getall()
                    }
