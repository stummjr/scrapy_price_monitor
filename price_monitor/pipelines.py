# -*- coding: utf-8 -*-
from price_monitor import settings
from hubstorage import HubstorageClient
from price_monitor.utils import reversed_timestamp, get_product_names


class CollectionStoragePipeline(object):

    def open_spider(self, spider):
        client = HubstorageClient(auth=settings.SHUB_KEY)
        project = client.get_project('113789')
        self.data_stores = {}
        for product_name in get_product_names():
            self.data_stores[product_name] = project.collections.new_store(product_name)

    def process_item(self, item, spider):
        self.data_stores[item['product_name']].set({'_key': reversed_timestamp(), 'value': item})
        return item
