import json
import pkgutil
import scrapy
from datetime import datetime


class BaseSpider(scrapy.Spider):

    def start_requests(self):
        products = json.loads(pkgutil.get_data("price_monitor", "resources/urls.json").decode())
        for product_name in products:
            for url in products.get(product_name):
                if self.name in url:
                    item = {'product': product_name, 'timestamp': datetime.now().timestamp()}
                    yield scrapy.Request(url, meta={'item': item})
