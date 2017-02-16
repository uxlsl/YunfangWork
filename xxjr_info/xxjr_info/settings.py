# -*- coding: utf-8 -*-

# Scrapy settings for xxjr_info project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import xxjr_info.globalvar as Globalvar

global_spider = Globalvar.GlobalVar()

BOT_NAME = 'xxjr_info'

SPIDER_MODULES = ['xxjr_info.spiders']
NEWSPIDER_MODULE = 'xxjr_info.spiders'
COMMANDS_MODULE = 'xxjr_info.commands'



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xxjr_info (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 6

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = { 'Host': 'phone.xxjr.com',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Proxy-Connection': 'keep-alive',
'X-Requested-With': 'XMLHttpRequest',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-cn',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Origin': 'https://phone.xxjr.com',
'Connection': 'keep-alive',
'Referer': 'https://phone.xxjr.com/cpQuery/app/xxjrEval/houseEval',
'Cookie': 'JSESSIONID=E8CACAF25ABFB2645FC09854D6CD4AD6'}

DOWNLOADER_MIDDLEWARES = {
    'xxjr_info.middlewares.RandomUserAgent': 1,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'xxjr_info.middlewares.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware':130,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware':120,
}



# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xxjr_info.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'xxjr_info.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'xxjr_info.pipelines.XxjrInfoPipeline': 300,
}

RETRY_ENABLED = True
RETRY_TIMES = 6
RETRY_HTTP_CODES = [500,403,501,502,503,504,400,408,404,411,413,302,407]


#REDIRECT_ENABLED = False

EXTENSIONS = {
   'scrapy.telnet.TelnetConsole': None,
   'xxjr_info.latencies.Latencies':None,
}

REDIS_START_URLS_AS_SET = True

COOKIES_ENABLED = False
COOKIES_DEBUG = True

DOWNLOAD_DELAY = 0.11
DOWNLOAD_TIMEOUT = 25
RANDOMIZE_DOWNLOAD_DELAY = True

#LOG_LEVEL = 'INFO'

USER_AGENTS = [
  "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.3.31 NetType/WIFI Language/zh_CN",]

REDIS_HOST = '192.168.6.10'

REDIS_PORT = 6379

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
