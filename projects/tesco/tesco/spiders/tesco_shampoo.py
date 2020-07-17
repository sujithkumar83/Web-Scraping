# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class TescoShampooSpider(scrapy.Spider):
    name = 'tesco_shampoo'
    allowed_domains = ['https://www.tesco.com']
    #start_urls = ['https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo']

    script= '''
        function main(splash, args)
            local num_scrolls = 10
            local scroll_delay = 1
            splash.private_mode_enabled=false
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            splash: on_request(function(request)
                request:set_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
                end)
            --#Pass the url as an argument
            url= args.url
            --#Open the website
            assert(splash:go(url))
            --#Wait for it load
            assert(splash:wait(3))
            
            splash:set_viewport_full()
            for _ = 1, num_scrolls do
                local height = get_body_height()
                for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
                end
            end
            return {
            
                --#return html
                html= splash:html()  
            }
            
            end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo", callback=self.parse, endpoint="execute",args={
            'lua_source': self.script
        })

    def parse(self, response):
        for product in response.xpath("//ul[@class='product-list grid']/li[contains(@class,'product-list--list-item')]"):
            yield {
                'id': product.xpath(".//@data-sku").get(),
                'prod_name': product.xpath("//div[@class='product-details--wrapper']/div/h3/a/text()").get(),
                'new_flag': product.xpath(".div[@class='product-widget--offer-flash']/p/strong/text()").get(),
                #'Qty': product.xpath(".//div[@class='fop-description']/span[@class='fop-catch-weight']/text()").get(),
                'discounted_price': product.xpath(".//div[@class='product-controls__wrapper']/form/div/div/div/div/div/span/span[@class='price-value']/text()").get(),
                'offer_desc': product.xpath("//div[@class='hidden-medium product-info-section-small']/div[@class='product-info-message-list']/div[@class='product-info-message']/p/text()").get(),
                'url': response.urljoin(product.xpath("//div[@class='product-details--wrapper']/div/h3/a/@href").get()),
                #'rating': product.xpath(".//div[@class='review-wrapper']/span[@class='fop-rating']/span[@class='fop-rating-inner']/@title").get(),
                'unit_price': product.xpath("//div[@class='product-controls__wrapper']/form/div/div/div/span/span[@class='value']/text()").get(),
                'unit_weight': product.xpath("//div[@class='product-controls__wrapper']/form/div/div/div/span[@class='weight']/text()").get(),
                #'availability': product.xpath(".//div/a/span[@class='fop-mark-oos fop-image-corner']/text()").get()
            }
