# scrapy api
#from DmozSpider import DmozSpider
from spiders.prize_spider import PrizeSpider

# scrapy api
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings

def spider_closing(spider):
    """Activates on spider closed signal"""
    reactor.stop()

settings = Settings()

# crawl responsibly
crawler = Crawler()

# stop reactor when spider closes
crawler.signals.connect(spider_closing, signal=signals.spider_closed)

crawler.configure()
crawler.crawl(prize_spider())
crawler.start()
reactor.run()
