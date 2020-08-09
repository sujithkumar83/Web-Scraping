import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from asda.items import AsdaItem
class AsdaImageDowloader(scrapy.Spider):
    name = 'imgdownloader'

    
    script= '''
        function main(splash, args)
            --splash.resource_timeout=300
            local num_scrolls = 2
            local scroll_delay = 2
            splash.private_mode_enabled=true
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
            assert(splash:wait(40))

            --splash:set_viewport_full()
            for _ = 1, num_scrolls do
                local height = get_body_height()
                for i = 1, 15 do
                scroll_to(0, height * i/15)
                assert(splash:wait(scroll_delay))
                end
            end
            return {
                --png=splash:png(),
                --#return html
                html= splash:html()  
            }
           
                       
        end
    '''
    lnk="https://groceries.asda.com/shelf/health-beauty/hair-care/shampoo-conditioner/shampoo/103730"    
    
    
    def start_requests(self):
      
        yield SplashRequest(url=self.lnk, callback=self.parse1, endpoint="execute",args={
            'timeout':1800,
            'lua_source': self.script
        })
        for i in range(1,4):
            lnk2="https://groceries.asda.com/shelf/health-beauty/hair-care/shampoo-conditioner/shampoo/103730?facets=shelf%3A103730%3A0000&nutrition=&sortBy=&page="+str(i*60)

            yield SplashRequest(url=lnk2, callback=self.parse1, endpoint="execute",args={
                'timeout':1800,
                'lua_source': self.script
            })


    def parse1(self, response):
        
        for product in response.xpath("//div[@class='co-lazy-product-container']/div[@class=' co-product-list']/ul[@class=' co-product-list__main-cntr']/li/div[@class='co-product']"):
            loader=ItemLoader(item=AsdaItem(), selector=product)
            asda_img_url = product.xpath(".//div[@class='co-item__col1']/button/img/@src").get()
            asda_prod_name = product.xpath(".//div/div[@class='co-item__title-container']/h3/a/text()").get() + ' ' + product.xpath(".//div[@class='co-item__volume-container co-item__items']/span/text()").get()
            loader.add_value('image_urls', asda_img_url)    
            loader.add_value('image_name', asda_prod_name)
            yield loader.load_item()
         