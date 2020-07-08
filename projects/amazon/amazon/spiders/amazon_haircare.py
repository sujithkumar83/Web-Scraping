# -*- coding: utf-8 -*-
import scrapy


class AmazonHaircareSpider(scrapy.Spider):
    name = 'amazon_haircare'
    allowed_domains = ['https://www.amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/b/ref=s9_acss_bw_cg_HairCar_2a1_w?node=74094031/']

    def parse(self, response):
        def parse(self, response):
            for product in response.xpath("//div[@class='s-main-slot s-result-list s-search-results sg-row']"):
                yield {
                    'id': product.xpath(".//div[@class='fop-item fop-item-offer']/@data-sku/text()").get(),
                    'prod_name': product.xpath(".//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']/a[@class='a-link-normal a-text-normal']/span[@class='a-size-base-plus a-color-base a-text-normal']/text()").get(),
                    'sponsored': product.xpath(".//div[@class='a-row a-spacing-micro']/span[@class='a-size-mini a-color-secondary']/text()").get(),
                    'url': response.urljoin(product.xpath("//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']/a[@class='a-link-normal a-text-normal']/@href").get()),
                    'offer_desc': product.xpath(".//a[@class='fop-row-promo promotion-offer']/span/text()").get(),
                    'rating': product.xpath(".//div[@class='a-row a-size-small']/span[1]/@aria-label").get(),
                    'raters': product.xpath(".//div[@class='a-row a-size-small']/span[2]/@aria-label").get(),
                    'discounted_price': product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
                    'orig_price': product.xpath(".//span[@class='a-price a-text-price']/span[@class='a-offscreen']/text()").get(),
                    'unit_price': product.xpath(".//span[@class='a-size-base a-color-secondary']/text()").get()


                }
