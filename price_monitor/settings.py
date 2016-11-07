# -*- coding: utf-8 -*-
import os

BOT_NAME = 'price_monitor'
SPIDER_MODULES = ['price_monitor.spiders']
NEWSPIDER_MODULE = 'price_monitor.spiders'

ROBOTSTXT_OBEY = True

SHUB_KEY = os.getenv('$SHUB_KEY')
AWS_ACCESS_KEY = os.getenv('$AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('$AWS_SECRET_KEY')

SHUB_JOBKEY = os.getenv('SHUB_JOBKEY', '').split('/')[0]

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'price_monitor.pipelines.CollectionStoragePipeline': 400,
}

AUTOTHROTTLE_ENABLED = True
# HTTPCACHE_ENABLED = True
