#!/bin/sh
#
#
echo "select last_update,title from shop_info order by last_update desc ;" | \
mysql --user=root --password=root --host=127.0.0.1 --port=13306 shop_database

# mysql> show columns from shop_info;
# mysql> select * from shop_info;
# mysql> drop table shop_info;
