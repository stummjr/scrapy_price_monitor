import json
import pkgutil
import scrapy
from datetime import datetime
from price_monitor.utils import get_product_names


class BaseSpider(scrapy.Spider):

    def start_requests(self):
        products = json.loads(pkgutil.get_data("price_monitor", "resources/urls.json").decode())
        for product_name in get_product_names():
            for url in products.get(product_name):
                if self.name in url:
                    item = {
                        'product_name': product_name,
                        'timestamp': datetime.now().timestamp(),
                        'retailer': self.name,
                    }
                    yield scrapy.Request(url, meta={'item': item})
