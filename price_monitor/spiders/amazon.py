from .base_spider import BaseSpider


class AmazonSpider(BaseSpider):
    name = "amazon"
    allowed_domains = ["amazon.com"]

    def parse(self, response):
        item = {}
        item['title'] = response.css("span#productTitle::text").extract_first("").strip()
        item['price'] = response.css("span#priceblock_ourprice::text").re_first("\$(.*)")
        item['rating'] = response.css('a#reviewStarsLinkedCustomerReviews > i > span::text').re_first("(.+) out of .+")
        yield item
