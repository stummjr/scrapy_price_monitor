"""Simple price monitor built with Scrapy and Scrapy Cloud
"""
import os
import json
import argparse
from hubstorage import HubstorageClient
from datetime import datetime, timedelta


def build_report(items):
    raise NotImplementedError('Report not implemented yet')


# should compare only from the same product
def get_items_from_last_n_hours(apikey, project_id, hours=24):
    project = HubstorageClient(apikey).get_project(project_id)
    item_store = project.collections.new_store('price_monitor_data')
    since_ts = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
    return list(item_store.get(meta=['_key', '_ts'], startts=since_ts))


def get_latest_item_from_store(last_n_hours_items, product, store):
    for item in last_n_hours_items:
        if (item.get('value', {}).get('product') == product and
                store in item.get('value', {}).get('url')):
            return item


def is_the_cheapest_from(item, last_n_hours_items):
    if float(item.get('value', {}).get('price')) == 0:
        return False
    lowest_in_interval = min(
        [float(x.get('value', {}).get('price')) for x in last_n_hours_items
            if x != item and
            x.get('value', {}).get('product') == item.get('value', {}).get('product')]
    )
    return float(item.get('value', {}).get('price')) < lowest_in_interval


def get_product_names():
    return list(
        # json.loads(pkgutil.get_data("price_monitor", "resources/urls.json").decode()).keys()
        json.load(open("price_monitor/resources/urls.json")).keys()
    )


def get_stores_for_product(product_name):
    def get_store_name_from_url(url):
        return url.split("://")[1].split("/")[0].replace("www.", "")

    data = json.load(open("price_monitor/resources/urls.json"))
    # open(pkg_resources.resource_filename("price_monitor", "resources/urls.json")))
    return {get_store_name_from_url(url) for url in data[product_name]}


def main(args):
    items = get_items_from_last_n_hours(args.apikey, args.project_id, args.days * 24)
    for product_name in get_product_names():
        for store in get_stores_for_product(product_name):
            item = get_latest_item_from_store(items, product_name, store)
            if is_the_cheapest_from(item, items):
                print('***** LOWEST PRICE FOUND!!! *****')


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--apikey', default=os.getenv('SHUB_KEY', None),
        help='API key to use for scrapinghub (fallbacks to SHUB_KEY variable)')
    parser.add_argument('project_id', type=int, help='Project ID to get info from.')
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to compare with the last price.')
    args = parser.parse_args()

    if not args.apikey:
        parser.error('Please provide an API key with --apikey option')
    return args


if __name__ == '__main__':
    main(parse_args())
