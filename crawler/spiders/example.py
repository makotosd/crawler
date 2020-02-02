# -*- coding: utf-8 -*-
import scrapy
from crawler.items import Post


class ExampleSpider(scrapy.Spider):
    name = 'zxy'
    allowed_domains = ['zxy.work']
    start_urls = ['https://zxy.work/']

    def parse(self, response):
        print("====> {}".format(response.url))
        # for quote in response.css('div.quote'):
        for quote in response.css('ul.locationsMapList li'):
            item = Post()
            # item['author'] = quote.css('small.author::text').extract_first()
            item['text'] = quote.css('::text').extract_first()
            item['url'] = quote.css('::attr("href")').extract_first()
            # item['tags'] = quote.css('div.tags a.tag::text').extract()

            url = response.urljoin(item['url'])
            print("=======> {}".format(url))
            item['adrs'] = scrapy.Request(url, callback=self.parse)

            yield item

        for quote in response.css('div#Map__gmap'):
            print("****** {}".format(response.url))

            '''
            < div id = "Map__gmap"
            class ="googleMap" data-office-address="埼玉県草加市高砂2-9-1" data-office-lat="35.8287494" data-office-lng="139.8045457" >
            </div>
            '''
            yield quote.css('::attr("data-office-address"')
