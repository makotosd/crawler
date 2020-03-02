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


def createDB():
    url = urlparse('mysql://root:root@127.0.0.1:13306/shop_database')  # for Ops
    # url = urlparse('mysql+pymysql://stock@localhost:3306/stockdb')  # for Dev

    conn = mysql.connector.connect(
        host=url.hostname,
        port=url.port,
        user=url.username,
        database=url.path[1:],
        password=url.password
    )

    ############################################################
    ## table 作成
    ############################################################
    sql = "CREATE TABLE IF NOT EXISTS queue_task (" \
          "cc char(64) NOT NULL," \
          "target_feature char(64) NOT NULL," \
          "num_of_neuron int unsigned NOT NULL, " \
          "num_train int NOT NULL," \
          "rnn char(64) NOT NULL," \
          "status char(64) NOT NULL," \
          "queued_at datetime," \
          "running_at datetime," \
          "finished_at datetime," \
          "PRIMARY KEY(cc, target_feature, num_of_neuron, rnn)" \
          ")"

    psql.execute(sql, conn)
    conn.commit()


def readJson():
    with open(JSONFILE) as f:
        df = json.load(f)
    for shop_info in df:
        print(shop_info)
        for key in shop_info:
            print("  {} {}".format(key, shop_info[key]))


def closeDB():
    pass


def do_main():
    createDB()
    readJson()
    closeDB()




if __name__ == "__main__":
    do_main()
