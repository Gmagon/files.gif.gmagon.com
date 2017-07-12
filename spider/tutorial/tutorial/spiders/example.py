# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor

import time

class QuotesSpider(CrawlSpider):

    name = "quotes"
    allowed_domains = [
        'sina.com.cn'
    ]

    rules =[
        Rule(LinkExtractor(allow=("http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_27/74766_784127_404552.gif")), follow=True, callback='parse_item')
    ]

    download_delay = 2

    def start_requests(self):
        urls = [
            'http://gif.sina.com.cn/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(2.5)
        page = response.url.split("/")[-2]

        list = response.css('img').xpath('@src').extract()
        for item in list:
            self.log('Saved file %s' % item)

        return
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)