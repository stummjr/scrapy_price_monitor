from .base_spider import BaseSpider


class BestbuySpider(BaseSpider):
    name = "bestbuy"
    allowed_domains = ["bestbuy.com"]

    def parse(self, response):
        item = {}
        item['url'] = response.url
        item['title'] = response.css("div#sku-title > h1 ::text").extract_first().strip()
        item['price'] = response.css('div.price-block ::attr(data-customer-price)').extract_first()
        item['rating'] = response.css("span.average-score ::text").extract_first()
        yield item
