# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse
import mysql.connector  # need to install mysql-connector-python
import pandas.io.sql as psql  # need to install pandas


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

    # デストラクタ
    def __del__(self):
        # DBとの切断
        self.conn.commit()
        self.conn.close()


    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        sql = ""  # select * from shop_info;"  # TODO: urlとtitleでSQLからselectする。
        result_mysql = psql.execute(sql, self.conn)
        record = result_mysql.fetchone()
        print(url, title, record)
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
