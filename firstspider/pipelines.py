# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from twisted.enterprise import adbapi
import MySQLdb.cursors
import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

logger = logging.getLogger(__name__)

class FirstspiderPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db = 'test',
            host = '172.19.136.200',
            port = 3306,
            user = 'yinzx',
            passwd = '1111',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
            )
    def process_item(self, item, spider):
        logger.info("ready to insert!")
        d = self.dbpool.runInteraction(self.insert_item,item)
        d.addErrback(self.handle_err)
        return d

    def insert_item(self,conn,item):
        #conn.execute('''delete from item_today''')
        conn.execute('''insert into item_today (ITEM_NAME,ITEM_DESC,ITEM_LINK) values (%s,%s,%s)''', (item['title'],item['desc'],item['link']))
        logger.info("insert complete!")

    def handle_err(self,e):
        logger.error('fail!')