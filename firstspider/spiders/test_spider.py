import scrapy
from firstspider.items import FirstspiderItem
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging

logger = logging.getLogger(__name__)

class PaiToday(scrapy.Spider):
    name = "test"
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com"
        
    ]

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
    name = 'test2'
    allowed_domains = ["suning.com"]
    start_urls = [
        "http://pai.suning.com/shanpai/tomorrow.htm"
    ]

    def parse(self,response):
        item = FirstspiderItem()
        for sel in response.xpath('//div[@class="list-img"]'):
            title = sel.xpath('a/@title').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('a/@title').extract()
            item['title'] = [t.encode('gbk') for t in title]
            item['link'] = [t.encode('gbk') for t in link]
            item['desc'] = [t.encode('gbk') for t in desc]
            logger.info(item) 
            yield item

        
             