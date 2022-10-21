import scrapy

class gas(scrapy.Spider):
    name='gas'
    
    def start_requests(self):
        yield scrapy.Request('https://www.gasbuddy.com/home?search=grants+pass&fuel=1&method=all&maxAge=0')

    def parse(self, response):
        products = response.css('div.GenericStationListItem-module__stationListItem___3Jmn4')
        for product in products:
            yield {
            'gas_station': response.css('h3.header__header3___1b1oq.header__header___1zII0.header__midnight___1tdCQ.header__snug___lRSNK.StationDisplay-module__stationNameHeader___1A2q8>a::text').get(),
            'price': response.css('span.text__xl___2MXGo.text__left___1iOw3.StationDisplayPrice-module__price___3rARL::text').get().replace('$',''),
            'address': response.css('div.StationDisplay-module__address___2_c7v::text').get()
            }