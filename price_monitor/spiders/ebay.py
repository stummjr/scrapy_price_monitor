from extruct.w3cmicrodata import MicrodataExtractor
from .base_spider import BaseSpider


class EbaySpider(BaseSpider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.EbayNormalizeTitlePipeline': 300,
            'price_monitor.pipelines.CollectionStoragePipeline': 400
        }
    }

    def parse(self, response):
        extractor = MicrodataExtractor()
        properties = extractor.extract(response.body_as_unicode()).get('items')[0].get('properties', {})
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = properties.get('name')
        item['price'] = float(
            properties.get('offers', {}).get('properties', {}).get('price', 0)
        )
        if 'aggregateRating' in properties:
            item['rating'] = properties.get('aggregateRating', {}).get('properties', {}).get('ratingValue')
        yield item
