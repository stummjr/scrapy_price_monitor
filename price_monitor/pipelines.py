# -*- coding: utf-8 -*-
from datetime import datetime
from price_monitor import settings
from hubstorage import HubstorageClient


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
        def reversed_timestamp():
            return str(int((datetime(5000, 1, 1) - datetime.now()).total_seconds()))

        self.storage.set({'_key': reversed_timestamp(), 'value': item})
