# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    latlng = {}

    def process_item(self, item, spider):
        s = str(item['lat']) + "_" + str(item['lng'])
        if s in self.latlng:  # 重なっていたら0.0001/0.0001度ずらす。
            item['lat'] += 0.0001
            item['lng'] += 0.0001
            print('location of "{}" is overlapped with "{}"'.format(item['title'], self.latlng[s]))
        else:
            pass
        self.latlng[s] = item['title']

        return item
