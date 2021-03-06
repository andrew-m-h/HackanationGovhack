import scrapy

class CheckPrizeSpider(scrapy.Spider):
    name = 'checkprize'
    allowed_domains = ['2016.hackerspace.govhack.org']
    start_urls = [
        'https://2016.hackerspace.govhack.org/prizes'
    ]

    def parser(self, response):
        f = open('checkprize', 'w')
        for name in response.xpath('//body/div/div/section/div/section/div/div/div/table/tbody/tr/td/a/text()').extract():
            f.write(name+"\n")
