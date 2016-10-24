import scrapy
import pkgutil


class BaseSpider(scrapy.Spider):

    def start_requests(self):
        for url in pkgutil.get_data("price_monitor", "resources/urls.txt").split():
            url = url.decode()
            if self.name in url:
                yield scrapy.Request(url)
