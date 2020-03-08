#!/bin/sh
#
#

scrapy crawl zxy | tee log.scrapy
python gen_shoplist.py

