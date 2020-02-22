#!/bin/sh
#
#
OLDFILE=old_base.json
NEWFILE=latest_base.json
NEWBASE=appear.json
DISAPPER=disappear.json

if [ -f $NEWFILE ] ; then mv $NEWFILE $OLDFILE ; fi
scrapy crawl zxy -o $NEWFILE 2>&1 | tee log.scrapy
python json_diff.py $OLDFILE $NEWFILE $NEWBASE $DISAPPER

echo "NEW BASE=========================================="
cat $NEWBASE

echo ""
echo "DISAPPER BASE=========================================="
cat $DISAPPER
