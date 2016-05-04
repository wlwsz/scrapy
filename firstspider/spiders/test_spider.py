#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider,DropItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
import logging
import sys
import json
import time
import os.path
import requests
import re

#动态添加items到python环境变量中，仅在程序运行时有效
try:
    itempath = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(itempath)
    #print sys.path
    from items import FirstspiderItem,ProductSitItem
    import settings
except Exception, e:
    raise ImportError("import items failed!")

logger = logging.getLogger(__name__)
timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
basedir = os.path.join(settings.BASEDIR,'%(name)s_%(time)s.csv') 
meta = {
        'splash':{
            'endpoint':'render.html',
            'args':{
                'wait':10,
                'images':1,
                'render_all':1
                }
            }
        }

class PaiToday(scrapy.Spider):
    name = "PaiToday"
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com"   
    ]
    csvurl = basedir %{'time':timestr,'name':name}      
    custom_settings = {
        'FEED_URI': 'file:///%s' %csvurl,
    }   
    def parse(self,response):
        filename = response.url.split('/')[-2] + ".html"
        cateIDlist = response.xpath('//span[contains(@class,"t-span")]/@cateid').extract()
        url='http://pai.suning.com/shanpai/channel/reloadChooseTabData.htm?cateId='
        for cateid in cateIDlist:
            logger.info(url+cateid)
            #yield scrapy.Request(url + cateid,callback=self.parse_content,meta=meta,dont_filter=True)  #add splash meta,same effect with below
            yield SplashRequest(url + cateid,callback=self.parse_content,dont_filter=True)      #invoke splashrequest
    def parse_content(self,response):
        for sel in response.xpath('//div[@class="list-text"]'):
            item = FirstspiderItem()
            title = sel.xpath('h2[@class="pr"]/a/@title').extract()
            desc = sel.xpath('p[@class="list-prompt"]/@title').extract()
            link = sel.xpath('h2[@class="pr"]/a/@href').extract()
            item['title'] = [t.encode("gbk") for t in title]    #solving the encodeing problem when export to csv 
            item['desc'] = [t.encode("gbk") for t in desc]
            item['link'] = [t.encode("gbk") for t in link]
            #logger.info(item) 
            yield item
class PaiTomorrow(scrapy.Spider):
    name = 'PaiTomorrow'
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com/shanpai/tomorrow.htm"
    ]

    csvurl = os.path.join(basedir,'%(name)s_%(time)s.csv') \
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
class SuningProduct(CrawlSpider):
    """docstring for SuningProduct"""
    name = 'SuningProduct'
    allowed_domains = [
        "www.suning.com",
        "product.suning.com",
        "list.suning.com",
    ]
    start_urls = [
        #"https://movie.douban.com/top250", #403 not resolved
        #"http://pindao.suning.com/city/diannao.htm",
        "http://list.suning.com/0-258004-0.html"
    ]

    rules = (
        Rule(LinkExtractor(allow=(u"http://product\.suning\.com/\d+\.html",),),callback="parse_item",),

    )
    
    csvurl = os.path.join(basedir,'%(name)s_%(time)s.csv') \
            %{'time':timestr,'name':name}
    custom_settings = {
        'FEED_URI': 'file:///%s' %csvurl,
    }
    
    def parse_start_url(self,response):
        item = FirstspiderItem()
        logger.info("crawled URL below:")
        logger.info(response.url)
        return item
    def parse_item(self,response):
        item = FirstspiderItem()
        title = response.xpath('//h1[@id="itemDisplayName"]/text()').extract()
        link = response.xpath('//*[@id="proPriceBox"]/div/span/text()').extract()
        logger.info(link)
        item['title'] = [t.encode('gbk') for t in title]
        item['link'] = [t.encode('gbk') for t in link]
        item['desc'] = response.url
        return item
class ProductSit(scrapy.Spider):
    name = "ProductSit"
    allowed_domains = "productsit.cnsuning.com"
    start_urls = [
        "http://productsit.cnsuning.com/0000000000/120800000.html",
    ]
    def parse(self,response):
        canbuy = response.xpath('//*[@id="buyNowAddCart"]/@name')
        if canbuy and response.status==200:
            item = ProductSitItem()
            item['link'] = response.url
            yield item
        for product in xrange(120800001,120899999):
            yield Request("http://icpssit.cnsuning.com/icps-web/getAllPriceFourPage/000000000%s_0000000000_010_0250101_1_pc_showSaleStatus.vhtm?callback=showSaleStatus" \
             %product,callback=self.parse_product,dont_filter=True)

    def parse_product(self,response):
        rlist = re.split('[\(\)]',response.body)
        rdict = json.loads(rlist[1])
        invstatus = rdict['saleInfo'][0]['invStatus']
        #self.log(type(invstatus))
        if response.status==200 and invstatus == "1":
            productid = rdict['saleInfo'][0]['partNumber'][-9:]
            item = ProductSitItem()
            item['link'] = "http://productsit.cnsuning.com/0000000000/%s.html" %productid
            yield item
        else:
            #self.log("can not use!",logging.ERROR)
            pass
        

if __name__ == '__main__':
    #define process to run spiders in the current script file 
    process = CrawlerProcess(get_project_settings())
    process.crawl(PaiToday)
    #process.crawl(PaiTomorrow)
    #process.crawl(SuningProduct)
    #process.crawl(ProductSit)
    process.start()
            
                



        
             