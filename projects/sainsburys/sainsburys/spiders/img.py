import scrapy
import logging
import re
import ftfy as ft
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from sainsburys.items import SainsburysItem
from scrapy.utils.log import configure_logging 
class SainsburysImageDowloader(scrapy.Spider):
    name = 'imgdownloader'
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
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
        string = string.replace('ML', '')
        string = string.replace('Ml', 'ml')
        string = string.replace(',', ' ')
        string = string.replace('-', ' ')
        string = string.replace('+', ' ')
        string = string.replace(':', ' ')
        #string="".join(sorted(string))
        #string = string.replace('shampoo', '') (doesnt work as most of the conditioners come into play which they shouldnt)
        #string = string.title() # normalise case - capital at start of each word
        string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single space
        # string = ' '+ string +' ' # pad names for ngrams...
        string = re.sub(r'[,-./]|\sBD',r'', string)
        return string
    def start_requests(self):
        yield SplashRequest(url="https://www.sainsburys.co.uk/shop/gb/groceries/health-beauty/shampoo-247823-44", callback=self.parse1, endpoint="execute",args={
            'timeout':1800,
            'lua_source': self.script
        })
    
    def parse1(self, response):
        for product in response.xpath("//ul[@class='productLister gridView']/li[@class='gridItem']/div[contains(@class,'product ')]"):
            loader=ItemLoader(item=SainsburysItem(), selector=product)
            sainsburys_img_url = response.urljoin(product.xpath(".//div/div/h3/a/img/@src").get())
            sainsburys_prod_name = product.xpath("normalize-space(.//div/div/h3/a/text()[1])").get()
            name= self.cleanup(sainsburys_prod_name)
            loader.add_value('image_urls', sainsburys_img_url)    
            loader.add_value('image_name',name)
            yield loader.load_item()  
        lnk2=response.xpath("//div[@class='pagination']/ul/li[@class='next']/a/@href").get()
        if lnk2:
            yield SplashRequest(url=lnk2, callback=self.parse1, endpoint="execute",args={
                'timeout':1800,
                'lua_source': self.script
            })