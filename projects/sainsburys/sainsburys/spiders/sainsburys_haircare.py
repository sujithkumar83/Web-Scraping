# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy_splash import SplashRequest

class SainsburysHaircareSpider(scrapy.Spider):
    name = 'sainsburys_haircare'
    #allowed_domains = ['https://www.sainsburys.co.uk']
    #start_urls = ['https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44']

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
            assert(splash:wait(10))
            
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
        yield SplashRequest(url="https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44", callback=self.parse, endpoint="execute",args={
            'timeout':1800,
            'lua_source': self.script
        })
    client="Sainsburys"
    category="Shampoo"
    time = datetime.now()
    def parse(self, response):
        for product in response.xpath("//ul[@class='productLister gridView']/li[@class='gridItem']/div[contains(@class,'product ')]"):
            yield {
                'client': self.client,
                'time': self.time,
                'category': self.category,
                'id': product.xpath(".//div[@class='productNameAndPromotions']/div[@class='FM_suitability_indicator']/@barcode").get(),
                'sainsburys_prod_name': product.xpath("normalize-space(.//div/div/h3/a/text()[1])").get(),
                'sainsburys_discounted_price': product.xpath("normalize-space(.//div/div/div/div[contains(@class,'priceTab ')]/div/p[@class='pricePerUnit']/text()[1])").get(),
                'sainsburys_offer_desc': product.xpath(".//div/div[@class='productNameAndPromotions']/div[@class='promotion']/p/a/text()[1]").get(),     
                'sainsburys_url': product.xpath(".//div/div/h3/a/@href").get(),
                'sainsburys_rating': product.xpath(".//div/div/div/div/div[@class='reviews']/a/img/@alt").get(),           
                'sainsburys_unit_price': product.xpath(".//div[@class='addToTrolleytabContainer addItemBorderTop']/div/div/div/p[@class='pricePerMeasure']/text()[1]").get(),
                'sainsburys_availability': product.xpath(".//div[@class='messageBox']/p/text()").get(),
                
            }
        
        lnk2=response.xpath("//div[@class='pagination']/ul/li[@class='next']/a/@href").get()
        if lnk2:
            yield SplashRequest(url=lnk2, callback=self.parse, endpoint="execute",args={
                'timeout':1800,
                'lua_source': self.script
            })
