import scrapy
import logging
import re
import ftfy as ft
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.utils.log import configure_logging
from waitrose.items import WaitroseItem
import chompjs

class WaitroseImageDowloader(scrapy.Spider):
    name = 'imgdownloader'
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
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
            assert(splash:wait(25))
            
            if splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")~= nil then
                element = splash:select("body > div:nth-child(6) > div > div > div > section > div.acceptCookieCTA___NwqHh > button:nth-child(1)")
                element:mouse_click()
                splash:wait(10)
                
            end 
            n=0
            while (splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")~=nil) do
                local load_more=splash:select("#tSr > div > div.loadMoreWrapper___UneG1 > button")  
                load_more:mouse_click()
                assert(splash:wait(10))
                local height = get_body_height()
                for i = 1, n*10 do
                    scroll_to(0, height * i/10/n)
                    assert(splash:wait(2))
                end
            end
            
            splash:set_viewport_full()

            return {
                    --png=splash:png(),
                --#return html
                html= splash:html()  
            }
            
                        
        end
        
        '''
    frtoeng = "".maketrans("àâçéèêîôùû", "aaceeeiouu")
    def cleanup(self, string):
        string = ft.fix_text(string) # fix text encoding issues
        string = string.translate(self.frtoeng)
        string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
        string = string.lower() #make lower case
        chars_to_remove = [")","(",".","|","[","]","{","}","'","`","/","~"]
        rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
        string = re.sub(rx, '', string) #remove the list of chars defined above
        string = string.replace('&', '')
        string = string.replace('and', '')
        string = string.replace('ml', '')
        string = string.replace('Ml', 'ml')
        string = string.replace(',', ' ')
        string = string.replace('-', ' ')
        string = string.replace('+', ' ')
        #string="".join(sorted(string))
        #string = string.replace('shampoo', '') (doesnt work as most of the conditioners come into play which they shouldnt)
        #string = string.title() # normalise case - capital at start of each word
        string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single space
        # string = ' '+ string +' ' # pad names for ngrams...
        string = re.sub(r'[,-./]|\sBD',r'', string)
        return string

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
            
            waitrose_img_url = product.xpath(".//div/section/div[contains(@class, 'image___1aDKB')]/a/div[contains(@class, 'placeholder___2ydJA')]/div[contains(@class, 'LazyLoad ')]/picture/div/img/@src").get()
            waitrose_prod_name = product.xpath(".//@data-product-name").get()+ ' '+ product.xpath(".//div/section/header/a/span/text()").get()
            name= self.cleanup(waitrose_prod_name)
            print(waitrose_img_url)
            loader=ItemLoader(item=WaitroseItem(), selector=product)
            loader.add_value('image_urls', waitrose_img_url)    
            loader.add_value('image_name', name)
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


    