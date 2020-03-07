# -*- coding: utf-8 -*-
#  店舗の情報ファイル(json)を読み込んで、mysqlに初期データベースと
#  して登録する。
#  一回しか使わないスクリプト。
#  今後のデータベースの更新は、scrapyから行う。
#
from urllib.parse import urlparse
import mysql.connector  # need to install mysql-connector-python
import pandas.io.sql as psql  # need to install pandas
import pandas as pd
from time import sleep
import argparse
from datetime import datetime
import json


JSONFILE = 'latest_base.json'

conn = ''

def createDB():
    url = urlparse('mysql://root:root@127.0.0.1:13306/shop_database')  # for Ops
    # url = urlparse('mysql+pymysql://stock@localhost:3306/stockdb')  # for Dev
    global conn
    conn = mysql.connector.connect(
        host=url.hostname,
        port=url.port,
        user=url.username,
        database=url.path[1:],
        password=url.password
    )

    ############################################################
    # table 作成
    ############################################################
    sql = "CREATE TABLE IF NOT EXISTS shop_info (" \
          "url varchar(255) NOT NULL," \
          "title varchar(128) NOT NULL," \
          "description varchar(255)," \
          "address varchar(255)," \
          "lat double," \
          "lng double," \
          "first_entry datetime NOT NULL," \
          "last_update datetime NOT NULL," \
          "shop_group varchar(64) NOT NULL," \
          "PRIMARY KEY(title, url)" \
          ")"

    psql.execute(sql, conn)
    conn.commit()


def readJson():
    global conn

    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    with open(JSONFILE) as f:
        df = json.load(f)
        for shop_info in df:
            print(shop_info)

            if 'address' not in shop_info:
                shop_info['address'] = ""

            keys = ",".join(['url', 'title', 'description', 'address', 'lat', 'lng',
                             'first_entry', 'last_update', 'shop_group'])
            values = '"%s","%s","%s", "%s", %f, %f, "%s", "%s", "%s"' % (
                        shop_info['url'], shop_info['title'], shop_info['desc'], shop_info['address'],
                        shop_info['lat'], shop_info['lng'], now, now, shop_info['group'])
            sql = "INSERT INTO {} ({}) VALUES ({});".format("shop_info", keys, values)
            print(sql)
            psql.execute(sql, conn)
            conn.commit()


def closeDB():
    global conn
    conn.close()


def do_main():
    createDB()
    readJson()
    closeDB()


if __name__ == "__main__":
    do_main()
