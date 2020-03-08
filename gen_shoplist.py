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


JSON_shop = 'latest_shop.json'

conn = ''

def openDB():
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


# json.dumpはdatatime型やdate型を変換できないので、
# defaultで渡す関数を定義することが必要。
def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime)):  # (datetime, date)
        return obj.isoformat()
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))


def readDB():
    global conn

    today = datetime.now().strftime("%Y/%m/%d 00:00:00")

    sql = 'SELECT * FROM {} WHERE last_update > "{}";'.format("shop_info", today)
    print(sql)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    # result_mysql = psql.execute(sql, conn)
    record = cursor.fetchall()
    with open(JSON_shop, 'w') as f:
        json.dump(record, f, indent=4, default=json_serial)


def closeDB():
    global conn
    conn.close()


def do_main():
    openDB()
    readDB()
    closeDB()


if __name__ == "__main__":
    do_main()
