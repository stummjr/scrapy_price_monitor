# -*- coding: utf-8 -*-
from price_monitor import settings
from hubstorage import HubstorageClient
from price_monitor.utils import reversed_timestamp


class EbayNormalizeTitlePipeline(object):

    def process_item(self, item, spider):
        prefix = 'Details about'
        if item.get('title').startswith(prefix):
            item['title'] = item.get('title').replace(prefix, '').strip()
        return item


class CollectionStoragePipeline(object):

    def open_spider(self, spider):
        client = HubstorageClient(auth=settings.SHUB_KEY)
        project = client.get_project('113789')
        self.storage = project.collections.new_store('price_monitor_data')

    def process_item(self, item, spider):
        self.storage.set({'_key': reversed_timestamp(), 'value': item})
        return item
