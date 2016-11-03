# -*- coding: utf-8 -*-
import os

BOT_NAME = 'price_monitor'
SPIDER_MODULES = ['price_monitor.spiders']
NEWSPIDER_MODULE = 'price_monitor.spiders'

ROBOTSTXT_OBEY = True

SHUB_KEY = os.environ.get('$SHUB_KEY')
AWS_ACCESS_KEY = os.environ.get('$AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('$AWS_SECRET_KEY')

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'price_monitor.pipelines.CollectionStoragePipeline': 400,
}

AUTOTHROTTLE_ENABLED = True
# HTTPCACHE_ENABLED = True
