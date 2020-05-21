# -*- coding: utf-8 -*-

# Scrapy settings for movietest2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'movietest2'

SPIDER_MODULES = ['movietest2.spiders']
NEWSPIDER_MODULE = 'movietest2.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'movietest2 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
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
DEFAULT_REQUEST_HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    'Cookie':'bid=9JMhtyhKwCI; gr_user_id=dfc4a657-74ee-4905-90d1-afdcc278240c; _vwo_uuid_v2=D817A52A7B1A438F346CA5145718FC70D|11c7965ceae6dae41bda579ad8cc07ad; _ga=GA1.2.704102812.1568950460; ll="118254"; __yadk_uid=KJcw8kSGqgo0bzV13fiv89IQHblmzQnp; trc_cookie_storage=taboola%2520global%253Auser-id%3D6db6843a-c51d-4dd1-929b-c64a9d65c502-tuct47b1992; __gads=ID=3f19cf254ba723db:T=1572747084:S=ALNI_Mao2HHyRrl7R9fbqqQ-8L9y6ur9jw; douban-fav-remind=1; push_noty_num=0; push_doumail_num=0; viewed="34839848_26337727_30136932_26342364_1234142_26416562_2061116_26827295"; __utmz=30149280.1588833276.3.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="175718936:oI/7dGsQRCM"; __utmv=30149280.17571; ck=eH3o; __utmc=30149280; __utmc=223695111; ct=y; __utma=30149280.704102812.1568950460.1589080211.1589087550.8; __utmb=30149280.2.10.1589087550; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1589087552%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.704102812.1568950460.1589080211.1589087552.41; __utmb=223695111.0.10.1589087552; __utmz=223695111.1589087552.41.22.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=3297dbc060884462.1570180143.41.1589088238.1589080924.'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'movietest2.middlewares.Movietest2SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'movietest2.middlewares.Movietest2DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'movietest2.pipelines.Movietest2Pipeline': 300,
    'movietest2.pipelines.Movietest2FilePipeline':400
}


MONGO_URI='localhost:27017'
MONGO_DATABASE='Movie'


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
