import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from pttcc.items import PttccItem

class GossipingSpider(scrapy.Spider):
    name = "Gossiping"
    allowed_domains = ["ptt.cc"]
    pages = 21
    current_page = 0
    domain = 'https://www.ptt.cc'
    url = '/bbs/Gossiping/index.html'
    item = PttccItem()

    def start_requests(self):
        yield scrapy.Request(url=self.domain + self.url, callback=self.age_check)

    def age_check(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            yield FormRequest.from_response(response,
                                            formdata={'yes':'yes'},
                                            callback=self.parse,
                                            errback=self.errback,
                                            dont_filter=True)
        else:
            print("failed")

    def parse(self, response):
        print("success")

        gossiping_title = response.xpath('//div[@class="title"]/a/text()').extract()
        gossiping_url = response.xpath('//div[@class="title"]/a/@href').extract()

        self.item['title'] = gossiping_title
        self.item['url'] = gossiping_url
        self.current_page += 1

        print(self.item.items)

        if self.pages > self.current_page:
            prev_page_url = response.xpath('//a[contains(text(), "上頁")]/@href').extract_first()
            self.url = prev_page_url
            yield scrapy.Request(url=self.domain + self.url, callback=self.parse)
        else:
            print(self.item.items)

        # print(prev_page)
        # print(hardware_sale_details)
        # for detail in hardware_sale_details:
        #     yield scrapy.Request(url='https://www.ptt.cc' + detail, callback=self.parse_detail)
        # print(response.css('.r-ent .title a::text').extract())

    def errback(self, failure):
        # logs failures
        self.logger.error(repr(failure))

    def parse_detail(self, response):
        # 整篇文章拉回來
        print(response.xpath('//div[@id="main-content"]/text()').extract())
        # print(response.css('.article-metaline span.article-meta-value::text').extract())
        # print(Selector(response=response).xpath('//span[contains(text(), "@")]').extract())