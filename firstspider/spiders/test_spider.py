import scrapy
#from firstspider.items import FirstspiderItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider,DropItem
import logging
import json
import time
import os.path

logger = logging.getLogger(__name__)
timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())

class FirstspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

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
        for sel in response.xpath('//h2[@class="pr"]'):
            item = FirstspiderItem()
            title = sel.xpath('a/text()').extract()
            desc = sel.xpath('a/@title').extract()
            link = sel.xpath('a/@href').extract()
            item['title'] = [t.encode("gbk") for t in title]    #solving the encodeing problem when export to csv 
            item['desc'] = [t.encode("gbk") for t in desc]
            item['link'] = [t.encode("gbk") for t in link]
            logger.info(item) 
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
            item['title'] = [t.encode('gbk') for t in title]
            item['link'] = [t.encode('gbk') for t in link]
            item['desc'] = [t.encode('gbk') for t in desc]
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
                item['title'] = titem['itemName'].encode('gbk')
                item['link'] ="http://pai.suning.com/shanpai/detail/d/%s-2.htm" %titem['itemId']
                item['desc'] = titem['itemName'].encode('gbk')
                yield item
        else:
            raise CloseSpider("no items!")
            #logger.error("There is no more item!")

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(PaiToday)
    process.crawl(PaiTomorrow)
    process.start()
            
                



        
             