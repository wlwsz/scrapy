#-*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider,DropItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import logging
import sys
import json
import time
import os.path

#add moudle items into sys.path  
try:
    itempath = os.path.dirname(os.path.dirname(__file__))
    #print itempath
    sys.path.append(itempath)
    #print sys.path
    from items import FirstspiderItem
except Exception, e:
    raise ImportError("import items failed!")

logger = logging.getLogger(__name__)
timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())

class PaiToday(scrapy.Spider):
    name = "PaiToday"
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com"   
    ]
    
    csvurl = os.path.join(os.path.dirname(os.path.abspath(__file__)),'%(name)s_%(time)s.csv') \
            %{'time':timestr,'name':name}
    custom_settings = {
        'FEED_URI': 'file:///%s' %csvurl,
    }
    
    def parse(self,response):
        filename = response.url.split('/')[-2] + ".html"
        cateIDlist = response.xpath('//span[@class="t-span"]/@cateid').extract()
        url='http://pai.suning.com/shanpai/channel/reloadChooseTabData.htm?cateId='
        for cateid in cateIDlist:
            logger.info(url+cateid)
            yield Request(url + cateid,callback=self.parse_content)

    def parse_content(self,response):
        for sel in response.xpath('//div[@class="list-text"]'):
            item = FirstspiderItem()
            title = sel.xpath('h2[@class="pr"]/a/@title').extract()
            desc = sel.xpath('p[@class="list-prompt"]/@title').extract()
            link = sel.xpath('h2[@class="pr"]/a/@href').extract()
            item['title'] = [t.encode("utf-8") for t in title]    #solving the encodeing problem when export to csv 
            item['desc'] = [t.encode("utf-8") for t in desc]
            item['link'] = [t.encode("utf-8") for t in link]
            #logger.info(item) 
            yield item
class PaiTomorrow(scrapy.Spider):
    name = 'PaiTomorrow'
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com/shanpai/tomorrow.htm"
    ]

    csvurl = os.path.join(os.path.dirname(os.path.abspath(__file__)),'%(name)s_%(time)s.csv') \
            %{'time':timestr,'name':name}
    custom_settings = {
        'FEED_URI': 'file:///%s' %csvurl,
    }
    

    def parse(self,response):
        item = FirstspiderItem()
        for sel in response.xpath('//div[@class="list-img"]'):
            title = sel.xpath('a/@title').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('a/@title').extract()
            item['title'] = [t.encode('utf-8') for t in title]
            item['link'] = [t.encode('utf-8') for t in link]
            item['desc'] = [t.encode('utf-8') for t in desc]
            if "{{itemName}}" in item['title']:
                #raise DropItem('not a item!')
                pass
            else:
                yield item
        for i in range(1,10):
            url = "http://pai.suning.com/shanpai/tomorrow/find.htm?section=%s" %i
            yield Request(url,callback=self.parse_next)
    def parse_next(self,response):
        item = FirstspiderItem()
        itemdict = json.loads(response.body)
        #logger.info(response.body)
        if itemdict['result']['list']:
            itemlist = itemdict['result']['list']
            for titem in itemlist:
                item['title'] = titem['itemName'].encode('utf-8')
                item['link'] ="http://pai.suning.com/shanpai/detail/d/%s-2.htm" %titem['itemId']
                item['desc'] = titem['itemName'].encode('utf-8')
                yield item
        else:
            raise CloseSpider("no items!")
            #logger.error("There is no more item!")
class TestSpider(CrawlSpider):
    """docstring for TestSpider"""
    name = 'test'
    allowed_domains = "suning.com"
    start_urls = [
        #"https://movie.douban.com/top250", #403 not resolved
        #"http://pindao.suning.com/city/diannao.htm",
        "http://list.suning.com/0-258004-0.html"
    ]

    rules = [
        Rule(LinkExtractor(allow=(u"http://product\.suning\.com/\d+\.html",)),callback="parse_test"),

    ]
    '''
    csvurl = os.path.join(os.path.dirname(os.path.abspath(__file__)),'%(name)s_%(time)s.csv') \
            %{'time':timestr,'name':name}
    custom_settings = {
        'FEED_URI': 'file:///%s' %csvurl,
    }
    '''
    def parse(self,response):
        logger.info("crawled URL below:")
        logger.info(response.url)
    def parse_test(self,response):
        item = FirstspiderItem()
        title = sel.xpath('//h1[@id="itemDisplayName"]/text()').extract()
        link = sel.xpath('//dd[@id="netPrice"]/del/text()').extract()
        item['title'] = [t.encode('gbk') for t in title]
        item['link'] = [t.encode('gbk') for t in link]
        item['desc'] = [t.encode('gbk') for t in title]
        return item
        

if __name__ == '__main__':
    #define process to run spiders in the current script file 
    process = CrawlerProcess(get_project_settings())
    process.crawl(PaiToday)
    process.crawl(PaiTomorrow)
    process.crawl(TestSpider)
    process.start()
            
                



        
             