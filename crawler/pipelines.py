# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    latlng = {}

    def process_item(self, item, spider):
        s = str(item['lat']) + "_" + str(item['lng'])
        if s in self.latlng:
            item['lat'] += 0.001
            print('location of "{}" is overlaped with "{}"'.format(item['title'], self.latlng[s]))
        else:
            pass
        self.latlng[s] = item['title']

        return item
