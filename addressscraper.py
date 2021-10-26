import csv
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from addressscraper.spiders.torontoaddressbot import TorontoaddressbotSpider



def fetchRandomAddress():
    process = CrawlerProcess(get_project_settings())
    process.crawl(TorontoaddressbotSpider)
    process.start()

    
fetchRandomAddress()