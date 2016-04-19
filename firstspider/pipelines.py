# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FirstspiderPipeline(object):
    def process_item(self, item, spider):
        if "{{" in item['link']:
            raise DropItem('not a item')
        else:
            return item
