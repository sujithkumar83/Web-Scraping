import scrapy
import chompjs
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from tesco.items import TescoItem
class TescoImageDowloader(scrapy.Spider):
    name = 'imgdownloader'
    
    allowed_domains = ['https://www.tesco.com']
    
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/haircare/shampoo', callback=self.parse1, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            })
    
    def traversen(self,val):
        
        if isinstance(val, dict):
            
            for _ ,v in val.items():
                if ("title" in val.keys()) and ("defaultImageUrl" in val.keys()):
                    yield val
                else:
                    yield from self.traversen(v)
        elif isinstance(val, list):
            
            for v in val:
                yield from self.traversen(v)

    
    def parse1(self, response):
        jsonresp= chompjs.parse_js_object(response.xpath("//@data-redux-state").extract_first())

        

        for items in self.traversen(jsonresp):
            loader=ItemLoader(item=TescoItem(), selector=items)
            tesco_img_url=" "
            tesco_prod_name=" "
            tesco_img_url = items['defaultImageUrl']
            tesco_prod_name = items['title'] 
            print(tesco_img_url)
            loader.add_value('image_urls', tesco_img_url)    
            loader.add_value('image_name', tesco_prod_name)
            yield loader.load_item()  
        next_url= response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get()
        if next_url:
            next_lnk= response.urljoin(response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get())
            yield scrapy.Request(url=next_lnk, callback=self.parse1, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            },dont_filter=True)
    
    # def parse1(self, response):
    #     for product in response.xpath("//ul[@class='product-list grid']/li[contains(@class,'product-list--list-item')]"):
    #         loader=ItemLoader(item=TescoItem(), selector=product)
    #         tesco_img_url = product.xpath(".//div/div/div/div/a/div/img/@srcset").get()
    #         #tesco_img_url = tesco[tesco.rfind("http"):tesco.rfind(" ")]
    #         tesco_prod_name = product.xpath(".//div[@class='product-details--wrapper']/div/h3/a/text()").get()
    #         print("********")
    #         print(tesco_img_url)
    #         print(tesco_prod_name)
    #         loader.add_value('image_urls', tesco_img_url)    
    #         loader.add_value('image_name',tesco_prod_name)
    #         yield loader.load_item()  
    #     next_url= response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get()
    #     if next_url:
    #         next_lnk= response.urljoin(response.xpath("//nav[@class='pagination--page-selector-wrapper']/ul/li/a[@class='pagination--button prev-next'][@aria-label='Go to results page']/@href").get())
    #         yield scrapy.Request(url=next_lnk, callback=self.parse1, headers={
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    #         },dont_filter=True)