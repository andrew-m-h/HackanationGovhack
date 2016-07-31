import scrapy

from govhack.items import PrizeItem

class PrizeSpider(scrapy.Spider):
    name = 'prizes'
    allowed_domains = ['portal.govhack.org']
    start_urls = [
        "http://portal.govhack.org/prizes.html"
    ]

    def parse(self, response):
        #national hacks
        item = PrizeItem()
        item['is_category'] = True
        prize_categories = response.xpath('//body/div/div/div[@class="col-xs-12 col-sm-8 main-content"]/section[not(@id="portfolio")]/div/div[@class="row header-row"]/div/h1/text()').extract()

        i = 0
        for category in response.xpath('//body/div/div/div[@class="col-xs-12 col-sm-8 main-content"]/section[not(@id="portfolio")]/div/div[@class="row"]'):
            item['prize_name'] = category.xpath('div/div/h4[@class="media-heading"]/a/text()').extract()
            item['category'] = prize_categories[i]
            i += 1
            if item['category'] != 'Regional Prizes':
                yield item
                for href in category.xpath('div/div/h4[@class="media-heading"]/a/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, callback=self.parse_prize)

        #regional hacks
        states = response.xpath('//body/div/div/div[@class="col-xs-12 col-sm-8 main-content"]/section[not(@id="portfolio")]/div/div[@class="row"]/div/h1/a/text()').extract()

        state_counter = 0
        for state in response.xpath('//body/div/div/div[@class="col-xs-12 col-sm-8 main-content"]/section[not(@id="portfolio")]/div/div[@class="row"]/div[@class="row dataset-org"]'):
            regions = state.xpath('div')
            item['prize_name'] = regions[0].xpath('div/div/h4/a/text()').extract()
            item['category'] = states[state_counter]
            state_counter += 1
            yield item

            for href in regions[0].xpath('div/div/h4/a/@href'):
               url = response.urljoin(href.extract())
               yield scrapy.Request(url, callback=self.parse_prize)

            for region in regions[1:]:
                item['prize_name'] = region.xpath('div/div/h4/a/text()').extract()
                item['category'] = region.xpath('h2/a/text()').extract()[0]
                yield item
                for href in region.xpath('div/div/h4/a/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, callback=self.parse_prize)


    def parse_prize(self, response):
        item = PrizeItem()
        item['is_category'] = False
        item['prize_name']  = response.xpath('//body/div/div/div/section/div/h2/text()').extract()[0]
        item['prize_value'] = response.xpath('//body/div/div/div/section/div/h1[@id="prize"]/following-sibling::p/text()').extract()[0]
        item['prize_descr'] = response.xpath('//body/div/div/div/section/div/p/text()').extract()[0]
        item['prize_website']     = response.url
        yield item
