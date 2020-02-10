# -*- coding: utf-8 -*-
import scrapy
from crawler.items import Post
import googlemaps  # pip install googlemap
import time
import requests  # conda install requests
import re

ZXY_DOMAIN = 'zxy.work'
WORKSTYLYING_DOMAIN = 'workstyling.jp'
NEWWORK_DOMAIN = 'newwork109.com'
APIKEYFILE='apikey.txt'
GOOGLEAPIKEY = ''


#
# short URLを元に戻す
#
def unshorten_url(url):
    '''
    'https://www.google.co.jp/maps/place/%E3%82%AA%E3%82%AB%E3%83%A0%E3%83%A9%E8%B5%A4%E5%9D%82%E3%83%93%E3%83%AB/@35.6748119,139.7365292,17z/data=!3m1!4b1!4m5!3m4!1s0x60188bb8bf513a39:0xcd72cdaea76c836d!8m2!3d35.6748119!4d139.7387179?hl=ja&shorturl=1'
    '''
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    latitude, longitude = re.search(r'@(.*?),(.*?)z', resp.url).groups()
    return latitude, longitude

class ExampleSpider(scrapy.Spider):
    name = 'zxy'
    allowed_domains = [ZXY_DOMAIN, WORKSTYLYING_DOMAIN, NEWWORK_DOMAIN]
    start_urls = ['https://zxy.work/', 'https://mf.workstyling.jp/share/', 'https://www.newwork109.com/post/station']
    # start_urls = ['https://www.newwork109.com/post/station']

    #
    # goole api keyを読み込む
    #
    global GOOGLEAPIKEY
    with open(APIKEYFILE) as f:
        l = f.readlines()
        GOOGLEAPIKEY = l[0].strip()

    #
    # ZXYの店舗ページのパース
    #
    def parse_zxy(self, response):
        item = Post()
        item['url'] = response.url
        item['title'] = response.css('h1.baseDetailName::text').extract_first()
        item['desc'] = response.css('title::text').extract_first()
        item['address'] = response.css('.googleMap::attr("data-office-address")').extract_first()
        item['lat'] = float(response.css('.googleMap::attr("data-office-lat")').extract_first())
        item['lng'] = float(response.css('.googleMap::attr("data-office-lng")').extract_first())
        item['group'] = "zxy"

        print(item['url'])
        print(item['title'])
        print(item['desc'])
        print(item['address'])
        print(item['lat'])
        print(item['lng'])
        print("")

        yield item

    #
    # WorkStylyingの店舗ページのパース
    #
    def parse_workstyling(self, response):
        item = Post()
        item['url'] = response.url
        item['title'] = response.css('h1.pagename__ttl::text').extract_first()
        item['desc'] = response.css('meta[name="description"]::attr("content")').extract_first()

        # item['address'] = response.css('.googleMap::attr("data-office-address")').extract_first()
        dts = response.css('div.p-share-office-access__detail dl dt::text').extract()
        dds = response.css('div.p-share-office-access__detail dl dd::text').extract()
        for dt, dd in zip(dts, dds):
            if dt == '住所':
                item['address'] = dd
                break

        gmaps = googlemaps.Client(key=GOOGLEAPIKEY)
        result = gmaps.geocode(item['address'])
        item['lat'] = result[0]["geometry"]["location"]["lat"]
        item['lng'] = result[0]["geometry"]["location"]["lng"]
        time.sleep(0.5)  # 連続してgeocodeを呼ぶと失敗するという噂。

        item['group'] = "workstyling"
        yield item

    #
    # NewWorkの店舗ページのパース
    #
    def parse_newwork(self, response):
        item = Post()
        item['url'] = response.url
        item['title'] = response.css('h2.store-name::text').extract_first()
        item['desc'] = response.css('meta[name="description"]::attr("content")').extract_first()

        shortURL = response.css('div.google-btn a::attr(href)').extract_first()
        (lat, lng) = unshorten_url(shortURL)

        item['lat'] = lat
        item['lng'] = lng
        time.sleep(0.5)  # 連続してgeocodeを呼ぶと失敗するという噂。

        item['group'] = "newwork"
        yield item


    #
    # TOPページのparse
    #
    def parse(self, response):
        if ZXY_DOMAIN in response.url:

            print('拠点一覧(ZXY):')
            links = response.css('ul.locationsMapList a::attr("href")').extract()

            for link in links:
                url = response.urljoin(link)
                print("---    {}".format(url))
                yield scrapy.Request(url, self.parse_zxy)

        elif WORKSTYLYING_DOMAIN in response.url:
            print('拠点一覧(WORKSTYLING)')

            '''     
            <ul class="place-foot-nav__lst">
            <li><a href="https://mf.workstyling.jp/share/office/yaesu/">八重洲  </a></li>
            '''
            links = response.css('ul.place-foot-nav__lst a::attr("href")').extract()
            for link in links:
                url = response.urljoin(link)
                print("--WS   {}".format(url))
                yield scrapy.Request(url, self.parse_workstyling)

        elif NEWWORK_DOMAIN in response.url:
            print('拠点一覧(NEW WORK)')
            '''
            <div id="store-top">
			    <ul class="store">
				<!-- リンクはリスト毎 -->
				<a href="/post/store/1636">
            '''
            links = response.css('div#store-top > ul.store > a::attr("href")').extract()
            for link in links:
                url = response.urljoin(link)
                print("--NW   {}".format(url))
                yield scrapy.Request(url, self.parse_newwork)

        else:
            pass

