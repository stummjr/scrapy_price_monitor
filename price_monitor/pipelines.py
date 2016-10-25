# -*- coding: utf-8 -*-


class EbayNormalizeTitlePipeline(object):
    def process_item(self, item, spider):
        prefix = 'Details about'
        if item.get('title').startswith(prefix):
            item['title'] = item.get('title').replace(prefix, '').strip()
        return item
