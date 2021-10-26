import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from streetaddress import StreetAddressFormatter, StreetAddressParser

class TorontoaddressbotSpider(scrapy.Spider):
    name = 'torontoaddressbot'
    allowed_domains = ['www.fakeaddressgenerator.com']
    start_urls = ['https://www.fakeaddressgenerator.com/Canada_Real_Random_Address/index/city/Toronto//']

    def parse(self, response):
        #Extracting the content using css selectors
        addr_parser = StreetAddressParser()
        for sel in response.css(".list-unstyled.real-list").xpath("//ul/li/p"):
            if "Address"in str(sel):
                item = AddressItem()
                try:
                    fulladdress = str(sel.extract()).replace("<span>Address</span>","").replace("<p>","").replace("</p>","").strip()
                    address  = addr_parser.parse(fulladdress)
                    print (fulladdress)
                    print (address)
                    item['fulladdress'] = fulladdress
                    item['streetaddress'] = address.get('house') + ',' + address.get('street_full')
                    #Workaround, Split on STATE Since that his common
                    item['city'] = str(address.get('other')).split("ON")[0]
                    item['state'] = 'ON'
                    item['country'] = 'CA'
                    item['zipcode'] = str(address.get('other')).split("ON")[1]
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
    fulladdress = scrapy.Field()