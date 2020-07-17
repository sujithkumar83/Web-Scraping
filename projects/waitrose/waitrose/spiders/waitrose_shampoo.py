# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class WaitroseShampooSpider(scrapy.Spider):
    name = 'waitrose_shampoo'
    allowed_domains = ['https://www.waitrose.com/']
    #start_urls = ['https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo']

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
        yield SplashRequest(url="https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo", callback=self.parse, endpoint="execute",args={
            'lua_source': self.script
        })
    

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
