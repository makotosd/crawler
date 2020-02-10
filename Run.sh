#!/bin/sh
#
#
if [ -f zxy.json ] ; then rm zxy.json ; fi
scrapy crawl zxy -o zxy.json
