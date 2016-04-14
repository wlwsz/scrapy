import scrapy
from firstspider.items import FirstspiderItem
from scrapy.http import Request
import logging

logger = logging.getLogger(__name__)

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["suning.org"]
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
        
             