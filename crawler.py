#!/usr/bin/env python3

import sys
import signal
import scrapy
from scrapy.crawler import CrawlerProcess
from collections import OrderedDict
import datetime
import os
import sqlite3 as lite

from bottle import run
import bonus


DB = bonus.DB
vowels = "aàeèéiíïoòóuúü"    # Catalan vowels (w/ accentuation)


class AraSpider(scrapy.Spider):
    '''
    Class scrapy for task crawler. Scratch all news URL and count
    the number of vowels for each article.
    '''
    name = 'ara'
    allowed_domains = ["ara.cat"]
    start_urls = ['http://www.ara.cat/rss/']

    def __init__(self, data={}, *args, **kwargs):
        super(AraSpider, self).__init__(*args, **kwargs)
        self.data = data

    def parse(self, response):
        for href in response.xpath('//item/link/text()'):
            full_url = href.extract()
            self.data[full_url] = 0
            yield scrapy.Request(full_url, callback=self.parse_vowels)
            
    def parse_vowels(self, response):        
        titular =  response.css('#heading h1::text').extract()[0].lower()
        subtitular = ''.join(response.css(
            '#heading .pg-bkn-nutfold.txt ::text').extract()).strip().lower()
        body = ''.join(response.css('.mce-body .mce::text').extract()).lower()
        # body xpath('//div[@class="mce-body"]//text()')
        text = ''.join((titular, subtitular, body))
        count_vowels = sum(c in vowels for c in text)
        self.data[response.url] = count_vowels


def persist(data, filename=DB):
    '''
    Bonus1: Persist the results in SQLite3.
    Struct of bd:
        Tablename: Data of the day (i.e., date280320016)
            Items: Id (Autoincrement)
                   Web
                   Vowels
    Extra: If table exist, update new news.
    '''

    table_name = datetime.datetime.utcnow().strftime('date%d%m%Y')
    create = not os.path.exists(filename)
    db = lite.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and "
                   "name=?",(table_name,))
    tables = cursor.fetchall()

    if create or len(tables) == 0:
        with db:            
            cursor.execute("CREATE TABLE " +  table_name + " ("
                    "Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                    "Web TEXT UNIQUE NOT NULL, "
                    "Vowels INTEGER NOT NULL)")
            cursor.executemany("INSERT INTO " + table_name + "(Web,Vowels)"
                               " VALUES(?, ?)", data.items())
        return "Persisted"
    else:
        with db:
            cursor.executemany("INSERT OR IGNORE INTO " + table_name +
                               "(Web,Vowels) VALUES(?, ?)", data.items())
        return "Updated"
                
                
if __name__ == "__main__":
                
    data = OrderedDict()

    # Create and run the crawler object
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': False,
        'COOKIES_ENABLED': False,
    })
    process.crawl(AraSpider, data=data)
    process.start()

    # Show each resource (key : value) representation
    for k, v in data.items():
        print('{0} : {1}'.format(k, v))

    # Bonus1, persist the results in SQLite
    print("Data {0} : OK".format(persist(data)))

    # Bonus1/Bonus3 run ReST API server
    def signal_handler(signal, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    run(host='localhost', port=8080)
