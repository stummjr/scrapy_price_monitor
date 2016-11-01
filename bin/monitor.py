"""Simple price monitor built with Scrapy and Scrapy Cloud
"""
import os
import argparse
from datetime import datetime, timedelta
from hubstorage import HubstorageClient
from price_monitor.utils import get_product_names, get_retailers_for_product


class ProductItems(object):

    def __init__(self, product_name, apikey, project_id, hours=24, price_threshold=0):
        self.product_name = product_name
        self.project = HubstorageClient(apikey).get_project(project_id)
        self.item_store = self.project.collections.new_store(product_name)
        self.load_items_from_last_n_hours(hours)
        self.deals_from_last_run = self.get_deals_from_last_run()
        self.price_threshold = price_threshold

    def load_items_from_last_n_hours(self, n=24):
        """Fetch items from the last n hours, starting from the newest
        """
        since_time = int((datetime.now() - timedelta(hours=n)).timestamp() * 1000)
        self.items = [item.get('value') for item in self.get_deals_newer_than(since_time)]

    def get_deals_newer_than(self, since_time):
        return list(self.item_store.get(meta=['_key', '_ts'], startts=since_time))

    def get_retailer_deal_from_last_run(self, retailer):
        """Returns the most recently extracted item from a given retailer
        """
        for item in self.items:
            if retailer in item.get('url'):
                return item

    def get_deals_from_last_run(self):
        """Returns the items that have been extracted in the most recent execution
        """
        latest = []
        for retailer in get_retailers_for_product(self.product_name):
            latest.append(self.get_retailer_deal_from_last_run(retailer))
        return latest

    def get_best_deal_from_last_run(self):
        return min(self.deals_from_last_run, key=lambda x: x.get('price'))

    def get_best_deal_so_far(self):
        """Returns the item with the best price from previous executions (not including)
           the items from the most recent one.
        """
        items = [item for item in self.items if item not in self.deals_from_last_run]
        return min(items, key=lambda x: x.get('price'))

    def got_best_deal_in_last_run(self):
        """Checks whether the best deal overall is from the most recent execution.
        """
        return self.get_best_deal() in self.get_deals_from_last_run()

    def get_best_deal(self):
        """Returns the item with the best overall price. self.price_threshold can be set to avoid
           considering minor price drops.
        """
        best_so_far = self.get_best_deal_so_far()
        best_from_last = self.get_best_deal_from_last_run()
        if best_from_last.get('price') + self.price_threshold < best_so_far.get('price'):
            return best_from_last
        else:
            return best_so_far


def main(args):
    for product_name in get_product_names():
        prod_items = ProductItems(product_name, args.apikey, args.project_id, 48, args.price_threshold)
        if prod_items.got_best_deal_in_last_run():
            print_report(prod_items.get_best_deal())


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
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to compare with the last price')
    parser.add_argument('--price_threshold', type=float, default=1.0,
                        help='A margin to avoid raising alerts with minor price drops')
    parser.add_argument('project_id', type=int, help='Project ID to get info from')

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
