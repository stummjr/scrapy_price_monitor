"""Simple price monitor built with Scrapy and Scrapy Cloud
"""
import json
import argparse
from datetime import datetime, timedelta

storage_path = "price_monitor/items.jl"


def print_report(item, items):
    print('\n***** LOWEST PRICE FOUND *****')
    print('Product: {}'.format(item.get('product')))
    print('Price: {}'.format(item.get('price')))
    print('URL: {}'.format(item.get('url')))
    print('Time: {}'.format(datetime.fromtimestamp(item.get('timestamp'))))
    print('-- History --')
    for item in items:
        print('{}'.format(datetime.fromtimestamp(item.get('timestamp'))))
        print('\tUS$ {}'.format(item.get('price')))


def is_cheaper_than_all(item, items):
    if float(item.get('price')) == 0:
        return False

    cheapest_in_interval = min(
        [float(x.get('price')) for x in items
            if x != item and x.get('product') == item.get('product')]
    )
    return float(item.get('price')) < cheapest_in_interval


def get_items_by_product(product_name, items):
    return [item for item in items if item.get('product') == product_name]


def get_latest_from_retailer(product_name, retailer, items):
    for item in sort_by_age(get_items_by_product(product_name, items)):
        if retailer in item.get('url'):
            return item


def get_retailers_for_product(product_name):
    def get_retailer_name_from_url(url):
        return url.split("://")[1].split("/")[0].replace("www.", "")

    data = json.load(open("price_monitor/resources/urls.json"))
    return {get_retailer_name_from_url(url) for url in data[product_name]}


def get_product_names():
    return list(json.load(open("price_monitor/resources/urls.json")).keys())


def get_items_newer_than(since_time, items):
    return [item for item in items if item.get('timestamp') >= since_time]


def sort_by_age(items):
    return sorted(items, key=lambda x: x.get('timestamp'), reverse=True)


def get_items_from_last_n_hours(itemsfile, n=24):
    """Fetch items from the last n hours, starting from the newest
    """
    items = [json.loads(s.strip()) for s in open(itemsfile)]
    since_time = int((datetime.now() - timedelta(hours=n)).timestamp())
    return sort_by_age(get_items_newer_than(since_time, items))


def main(args):
    items = get_items_from_last_n_hours(args.itemsfile, args.days * 24)
    for product_name in get_product_names():
        for retailer in get_retailers_for_product(product_name):
            item = get_latest_from_retailer(product_name, retailer, items)
            if item and is_cheaper_than_all(item, items):
                print_report(item, items)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to compare with the last price.')
    parser.add_argument('--itemsfile', type=str, default=storage_path,
                        help='Path to the file holding the scraped items')

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
