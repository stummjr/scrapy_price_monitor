"""Simple price monitor built with Scrapy and Scrapy Cloud
"""
import os
import argparse
from datetime import datetime, timedelta
from hubstorage import HubstorageClient
from price_monitor.utils import get_product_names, get_retailers_for_product


class ProductItems(object):

    def __init__(self, product_name, apikey, project_id, hours=24):
        self.product_name = product_name
        self.project = HubstorageClient(apikey).get_project(project_id)
        self.item_store = self.project.collections.new_store(product_name)
        self.load_items_from_last_n_hours(hours)

    def load_items_from_last_n_hours(self, n=24):
        """Fetch items from the last n hours, starting from the newest
        """
        since_time = int((datetime.now() - timedelta(hours=n)).timestamp() * 1000)
        self.items = [item.get('value') for item in self.get_deals_newer_than(since_time)]

    def get_deals_newer_than(self, since_time):
        return list(self.item_store.get(meta=['_key', '_ts'], startts=since_time))

    def get_best_deal(self):
        return min(self.items, key=lambda x: x.get('price'))

    def get_latest_deal_from_retailer(self, retailer):
        for item in self.items:
            if retailer in item.get('url'):
                return item

    def get_latest_deals(self):
        latest = []
        for retailer in get_retailers_for_product(self.product_name):
            latest.append(self.get_latest_deal_from_retailer(retailer))
        return latest


def main(args):
    for product_name in get_product_names():
        prod_items = ProductItems(product_name, args.apikey, args.project_id, 48)
        best_deal = prod_items.get_best_deal()
        if best_deal in prod_items.get_latest_deals():
            print_report(best_deal)


def print_report(item):
    print('\n***** LOWEST PRICE FOUND *****')
    print('Product: {}'.format(item.get('product_name')))
    print('Price: {}'.format(item.get('price')))
    print('URL: {}'.format(item.get('url')))
    print('Time: {}'.format(datetime.fromtimestamp(item.get('timestamp'))))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--apikey', default=os.getenv('SHUB_KEY', None),
        help='API key to use for scrapinghub (fallbacks to SHUB_KEY variable)')
    parser.add_argument('project_id', type=int, help='Project ID to get info from.')
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to compare with the last price.')

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
