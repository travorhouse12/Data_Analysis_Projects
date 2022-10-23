import scrapy

class gasscraper(scrapy.Spider):
    name='gas'
    
    start_urls = ['https://www.gasbuddy.com/home?search=grants+pass&fuel=1&method=all&maxAge=0']

    def parse(self, response):
        for station in response.css('div.GenericStationListItem-module__stationListItem___3Jmn4'):
            yield {
                'name': station.css('h3.header__header3___1b1oq.header__header___1zII0.header__midnight___1tdCQ.header__snug___lRSNK.StationDisplay-module__stationNameHeader___1A2q8>a::text').get(),
                'price': station.css('span.text__xl___2MXGo.text__left___1iOw3.StationDisplayPrice-module__price___3rARL::text').get().replace('$',''),
                'price_submitted': station.css('span.ReportedBy-module__postedTime___J5H9Z::text').get(),
                'address': station.css('div.StationDisplay-module__address___2_c7v::text').get()

            }
            next_page = response.css('a.button__button___fo2tk.forms__field___E4Q71.forms__formControlBase___3Cl7I.button__fluid___2ez5a.button__secondary___1xuZs.button__branded___3hDeX').attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)