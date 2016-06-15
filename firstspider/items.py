# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from mytest.models import ProductSitItem


class FirstspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class ProductSitItem(scrapy.Item):
    proname = scrapy.Field()
    link = scrapy.Field()


class TestItem(DjangoItem):
    """测试scrapy-djangoitem"""
    django_model = ProductSitItem
