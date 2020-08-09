# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from datetime import datetime

class WaitroseShampooSpider(scrapy.Spider):
    name = 'waitrose_shampoo'
    allowed_domains = ['https://www.waitrose.com/']
    #start_urls = ['https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo']

    script= '''
    function main(splash, args)
        local num_scrolls = 1
        local scroll_delay = 10
        splash.private_mode_enabled=true
        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        splash: on_request(function(request)
            request:set_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
            end)
        url= args.url
        --#Open the website
        assert(splash:go(url))
        --#Wait for it load
        assert(splash:wait(20))

        if splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")~= nil then
            element = splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")
            element:mouse_click()
            assert(splash:wait(20))
            --[[local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                assert(splash:wait(4))
            end]]--
        end 
        while (splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")~=nil) do
            local load_more=splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")  
            load_more:mouse_click()
            assert(splash:wait(15))
            local height = get_body_height()
            --[[for i = 1, 4 do
                scroll_to(0, height * i/4)
                assert(splash:wait(2))
            end]]--
        end
        
        splash:set_viewport_full()

        return {
                --png=splash:png(),
            --#return html
            html= splash:html()  
        }
           
                       
    end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo", callback=self.parse, endpoint="execute",args={
            'timeout':1800,
            'lua_source': self.script
        })
    
    client="Waitrose"
    category="Shampoo"
    time = datetime.now()
    def parse(self, response):
        for product in response.xpath("//main[@class='appMain___2G0oc']/div/div/div/div[contains(@class,'row')]/article"):
            yield {
                'client': self.client,
                'time': self.time,
                'category': self.category,
                'id': product.xpath(".//@id").get(),
                'prod_name': product.xpath(".//@data-product-name").get(),
                'waitrose_Qty': product.xpath(".//div/section/header/a/span/text()").get(),
                'waitrose_discounted_price': product.xpath(".//div/section/div/span[@data-test='product-pod-price']/span/text()").get(),
                'waitrose_offer_desc': product.xpath(".//div/section/header/div/div/div/a/p/span/text()").get(),     
                'waitrose_url': response.urljoin(product.xpath(".//div/sectio/header/a/@href").get()),
                'waitrose_rating': product.xpath(".//div/section/div/p/a/span/span/span/text()").get(),           
                'waitrose_unit_price': product.xpath(".//div/section/div/span[@class='pricePerUnit___1gifh priceInfo___1J8aK']/text()").get(),
                'waitrose_new_flag': product.xpath(".//div/section/div/div[@class='mt-badge-roundNew']/a/text()").get(),
                'waitrose_prod_name': product.xpath(".//@data-product-name").get()+ ' '+ product.xpath(".//div/section/header/a/span/text()").get()

                }
