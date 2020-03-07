# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse
import mysql.connector  # need to install mysql-connector-python
import pandas.io.sql as psql  # need to install pandas
from datetime import datetime
import googlemaps  # pip install googlemap


APIKEYFILE = 'apikey.txt'


class CrawlerPipeline(object):
    latlng = {}

    # コンストラクタ
    def __init__(self):
        # DBとの接続
        url = urlparse('mysql://root:root@127.0.0.1:13306/shop_database')  # for Ops
        self.conn = mysql.connector.connect(
            host=url.hostname,
            port=url.port,
            user=url.username,
            database=url.path[1:],
            password=url.password
        )
        self.now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # google API key
        with open(APIKEYFILE) as f:
            l = f.readlines()
            self.GOOGLEAPIKEY = l[0].strip()

    # デストラクタ
    def __del__(self):
        # DBとの切断
        self.conn.commit()
        self.conn.close()


    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        sql = 'SELECT * FROM shop_info WHERE url="%s" AND title="%s";' % (url, title)
        result_mysql = psql.execute(sql, self.conn)
        record = result_mysql.fetchall()
        if len(record) != 0:
            sql = 'UPDATE shop_info SET last_update="%s" WHERE url="%s"' % (self.now, url)
            psql.execute(sql, self.conn)
            self.conn.commit()
        else:
            # description
            if 'desc' not in item:
                item['desc'] = ""

            # address(ほんとは確定させたい)
            if 'address' not in item:
                item['address'] = ""

            # lat, lng
            if 'lat' not in item:
                gmaps = googlemaps.Client(key=self.GOOGLEAPIKEY)
                result = gmaps.geocode(item['address'])
                item['lat'] = float(result[0]["geometry"]["location"]["lat"])
                item['lng'] = float(result[0]["geometry"]["location"]["lng"])

            keys = ",".join(['url', 'title', 'description', 'address', 'lat', 'lng',
                             'first_entry', 'last_update', 'shop_group'])
            values = '"%s","%s","%s", "%s", %f, %f, "%s", "%s", "%s"' % (
                        item['url'], item['title'], item['desc'], item['address'],
                        item['lat'], item['lng'], self.now, self.now, item['group'])
            sql = "INSERT INTO {} ({}) VALUES ({});".format("shop_info", keys, values)
            psql.execute(sql, self.conn)
            self.conn.commit()
        '''
        s = str(item['lat']) + "_" + str(item['lng'])
        if s in self.latlng:  # 重なっていたら0.0001/0.0001度ずらす。
            item['lat'] += 0.0001
            item['lng'] += 0.0001
            print('location of "{}" is overlapped with "{}"'.format(item['title'], self.latlng[s]))
        else:
            pass
        self.latlng[s] = item['title']
        '''

        return item
