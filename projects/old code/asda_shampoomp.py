# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AsdaShampooSpider(scrapy.Spider):
    name = 'asda_shampoo'
    allowed_domains = ['https://groceries.asda.com']
    # start_urls = ['https://groceries.asda.com/shelf/health-beauty/hair-care/shampoo-conditioner/shampoo/103730']
    
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
    rule=(
        Rule(LinkExtractor(restrict_xpaths=),callback='parse_item', follow=True),
    )
    def start_requests(self):
        yield SplashRequest(url="https://groceries.asda.com/shelf/health-beauty/hair-care/shampoo-conditioner/shampoo/103730", callback=self.parse, endpoint="execute",args={
            'lua_source': self.script
        })

    def parse_item(self, response):
        for product in response.xpath("//div[@class=' co-product-list']/ul[@class=' co-product-list__main-cntr']/li/div[@class='co-product']"):
            yield {
                'id': product.xpath(".//div[@class='productNameAndPromotions']/div/@barcode").get(),
                'prod_name': product.xpath(".//div/div[@class='co-item__title-container']/h3/a/text()").getall(),
                'qty': product.xpath(".//div[@class='co-item__volume-container co-item__items']/span/text()").getall(),
                'discounted_price': product.xpath(".//strong[@class='co-product__price']/text()").get(),
                'offer_desc': product.xpath(".//span[@class='co-product__promo-text']/text()").get(),     
                'url': response.urljoin(product.xpath(".//div[@class='co-item__title-container']/h3/a/@href").get()),
                'rating': product.xpath(".//div[@class='rating-stars']/@aria-label").get(),           
                'unit_price': product.xpath(".//span[@class='co-product__price-per-uom']/text()").get(),
                'orig_price': product.xpath(".//span[@class='co-product__was-price']/text()").get()

                    }
        

      