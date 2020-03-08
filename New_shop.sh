#!/bin/sh
#
#
echo "select first_entry,title from shop_info order by first_entry ;" | \
mysql --user=root --password=root --host=127.0.0.1 --port=13306 shop_database

# mysql> show columns from shop_info;
# mysql> select * from shop_info;
# mysql> drop table shop_info;
