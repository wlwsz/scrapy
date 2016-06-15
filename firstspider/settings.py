# -*- coding: utf-8 -*-
import logging
import time
import os
import sys

sys.path.append("D:\python_code\django-pai")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mytest.settings'
# Scrapy settings for firstspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'firstspider'

SPIDER_MODULES = ['firstspider.spiders']
NEWSPIDER_MODULE = 'firstspider.spiders'
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'firstspider (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
## The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=32
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#    'firstspider.middlewares.MyCustomSpiderMiddleware': 543,
         
}
SPLASH_URL = 'http://172.19.136.199:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'firstspider.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy_crawlera.CrawleraMiddleware': 600 ,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}
#DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 600
CRAWLERA_ENABLED = False
CRAWLERA_USER = '3b187fa819cd4a149d2c328e6c83a97e'
CRAWLERA_PASS = ''
#CRAWLERA_PRESERVE_DELAY = True

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#   'firstspider.pipelines.FirstspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
AUTOTHROTTLE_ENABLED=False
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

csvurl = os.path.join(os.path.dirname(os.path.abspath(__file__)),'%(name)s_%(time)s.csv') 
FEED_URI='file:///%s' %csvurl
FEED_FORMAT='CSV'
'''
FEED_EXPORT_FIELDS=[
    'title',
    'desc',
    'link'
]
'''
#LOG_FILE= os.path.join(os.path.dirname(os.path.abspath(__file__)),'spider.log')
LOG_ENABLED = True
LOG_ENCODING = 'GBK'
LOG_LEVEL = logging.DEBUG
#FEED_EXPORTERS ={}
