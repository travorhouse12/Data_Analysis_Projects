import scrapy

class whiskycrapy(scrapy.Spider):
    name='whisky'
    start_urls = ['https://www.caskers.com/spirits/whiskey/']

    def parse(self, response):
        products = response.css('li.item product product-item')
        for product in products:
            item = {
            'brand': response.css('a.product-item-link::text').get(),
            'price': response.css('span.price::text').get().replace('$','')
            }
            yield item
        pass