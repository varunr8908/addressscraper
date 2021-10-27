import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from streetaddress import  StreetAddressParser
from geopy.geocoders import Nominatim

class TorontoaddressbotSpider(scrapy.Spider):
    name = 'torontoaddressbot'
    allowed_domains = ['www.fakeaddressgenerator.com']
    start_urls = ['https://www.fakeaddressgenerator.com/US_Real_Random_Address/index/state/MA/city/Boston/']

    def parse(self, response):
        #Extracting the content using css selectors
        addr_parser =  StreetAddressParser()
        geolocator = Nominatim(user_agent="addressscraper")
        for sel in response.css(".list-unstyled.real-list").xpath("//ul/li/p"):
            if "Address"in str(sel):
                item = AddressItem()
                try:
                    fulladdress = str(sel.extract()).replace("<span>Address</span>","").replace("<p>","").replace("</p>","").strip()
                    location = geolocator.geocode(fulladdress)
                    address  = addr_parser.parse(fulladdress)
                    
                    print('#location')
                    print(location.address)
                    print((location.latitude, location.longitude))
                    print('#fulladdress')
                    print (fulladdress)
                    print('#address')
                    print (address)
                    item['fulladdress'] = fulladdress
                    item['streetaddress'] = address.get('house') + ',' + address.get('street_full')
                    #Workaround, Split on STATE Since that his common
                    item['city'] = str(address.get('other')).split("MA")[0]
                    item['state'] = 'MA'
                    item['country'] = 'US'
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude
                    item['zipcode'] = str(address.get('other')).split("MA")[1]
                    #yield or give the scraped info to scrapy
                except:
                    continue
                yield item
    

class AddressItem(scrapy.Item):
    streetaddress = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    country = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    fulladdress = scrapy.Field()