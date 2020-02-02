# -*- coding: utf-8 -*-
import scrapy
from crawler.items import Post


class ExampleSpider(scrapy.Spider):
    name = 'zxy'
    allowed_domains = ['zxy.work']
    start_urls = ['https://zxy.work/']

    def parse_shop(self, response):
        item = Post()
        item['url'] = response.url
        item['title'] = response.css('h1.baseDetailName::text').extract_first()
        item['desc'] = response.css('title::text').extract_first()
        item['address'] = response.css('.googleMap::attr("data-office-address")').extract_first()
        item['lat'] = response.css('.googleMap::attr("data-office-lat")').extract_first()
        item['lng'] = response.css('.googleMap::attr("data-office-lng")').extract_first()

        print(item['url'])
        print(item['title'])
        print(item['desc'])
        print(item['address'])
        print(item['lat'])
        print(item['lng'])
        print("")

        yield item


    def parse(self, response):
        print('拠点一覧:')
        links = response.css('ul.locationsMapList a::attr("href")').extract()

        for link in links:
            url = response.urljoin(link)
            print("---    {}".format(url))
            yield scrapy.Request(url, self.parse_shop)

