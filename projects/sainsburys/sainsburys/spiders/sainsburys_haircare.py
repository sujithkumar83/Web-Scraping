# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class SainsburysHaircareSpider(scrapy.Spider):
    name = 'sainsburys_haircare'
    allowed_domains = ['https://www.sainsburys.co.uk']
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
        yield SplashRequest(url="https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44", callback=self.parse, endpoint="execute",args={
            'lua_source': self.script
        })
    def parse(self, response):
        for product in response.xpath("//ul[@class='productLister gridView']/li[@class='gridItem']"):
            yield {
                'id': product.xpath("//div[@class='productNameAndPromotions']/div[@class='FM_suitability_indicator']/@barcode").getall(),
                'prod_name': product.xpath("normalize-space(//div/div/div/h3/a/text()[1])").getall(),
                'discounted_price': product.xpath("//div/div/div/div/div[contains(@class,'priceTab ')]/div/p[@class='pricePerUnit']/text()[1]").getall(),
                'offer_desc': product.xpath("//div/div/div/div/p/a/text()").getall(),     
                'url': product.xpath("//div/div/div/h3/a/@href").getall(),
                'rating': product.xpath("//div/div/div/div/div/div[@class='reviews']/a/img/@alt").getall(),           
                'unit_price': product.xpath("//div/div[@class='addToTrolleytabContainer addItemBorderTop']/div/div/div/p[@class='pricePerMeasure']/text()[1]").getall(),
                'availability': product.xpath("//div[@class='messageBox']/p/text()").getall()
            }
