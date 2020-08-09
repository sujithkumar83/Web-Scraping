import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from waitrose.items import WaitroseItem
import chompjs

class WaitroseImageDowloader(scrapy.Spider):
    name = 'imgdownloader'

    
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
        assert(splash:wait(8))

        if splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")~= nil then
            element = splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")
            element:mouse_click()
            assert(splash:wait(10))
            local height = get_body_height()
            for i = 1, 5 do
                scroll_to(0, height * i/5)
                assert(splash:wait(2))
            end
        end
        y=1 
        while (splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")~=nil) do
            local load_more=splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")  
            load_more:mouse_click()
            assert(splash:wait(20))
            local height = get_body_height()
            for i = 1, 10*y do
                scroll_to(0, height * i/10/y)
                assert(splash:wait(2))
            end
            y=y+1
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
        yield SplashRequest(url="https://www.waitrose.com/ecom/shop/browse/groceries/toiletries_health_and_beauty/hair_care/shampoo", callback=self.parse1, endpoint="execute",args={
            'timeout':1800,
            'lua_source': self.script
        })
    # def traverse(self, val):
    #     if val.len() != 0:
    #         if isinstance(val, dict):
    #             for k, v in val.items():
    #                 if k=="products":
    #                     yield v
    #                 else:
    #                     yield from self.traverse(v)
    #         elif isinstance(val, list):
    #             for v in val:
    #                 yield from self.traverse(v)

    # def traversen(self,val):
            
    #     if isinstance(val, dict):
            
    #         for _ ,v in val.items():
    #             if ("thumbnail" in val.keys()) and ("size" in val.keys()) and ("name" in val.keys()):
    #                 yield val
    #             else:
    #                 yield from self.traversen(v)
    #     elif isinstance(val, list):
            
    #         for v in val:
    #             yield from self.traversen(v)

    
    def parse1(self, response):
        for product in response.xpath("//main[@class='appMain___2G0oc']/div/div/div/div[contains(@class,'row')]/article"):
            loader=ItemLoader(item=WaitroseItem(), selector=product)
            waitrose_img_url = product.xpath(".//section[@class='details___1fZBF']/div[@class='image___1aDKB']/a/div/div/picture/div/img/@src").get()
            waitrose_prod_name = product.xpath(".//@data-product-name").get()+ ' '+ product.xpath(".//div/section/header/a/span/text()").get()
            print(waitrose_img_url)
            loader.add_value('image_urls', waitrose_img_url)    
            loader.add_value('image_name', waitrose_prod_name)
            yield loader.load_item()
            


        # jsonresp= chompjs.parse_js_object(response.xpath("//script[contains(.,'medium')]/text()").extract_first())

        

        # for items in self.traversen(jsonresp):
        #     loader=ItemLoader(item=WaitroseItem(), selector=items)
        #     waitrose_img_url = items['thumbnail']
        #     waitrose_prod_name = items['name'] + ' ' + items['size']
        #     print(waitrose_img_url)
        #     loader.add_value('image_urls', waitrose_img_url)    
        #     loader.add_value('image_name', waitrose_prod_name)
        #     yield loader.load_item()  


    