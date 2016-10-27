import json
import unittest
from .. import monitor


class TestMonitor(unittest.TestCase):

    def setUp(self):
        with open('price_monitor/bin/tests/fixture-prices.json') as fp:
            self.prices_data = json.load(fp)

    def test_latest_item_from_store(self):
        item = monitor.get_latest_item_from_store(self.prices_data, 'webcam-logitech-c920', 'amazon')
        self.assertEqual(item.get('_key'), '94140084160.73326')
        item = monitor.get_latest_item_from_store(self.prices_data, 'webcam-logitech-c920', 'bestbuy')
        self.assertEqual(item.get('_key'), '94140084506.68796')
        item = monitor.get_latest_item_from_store(self.prices_data, 'webcam-logitech-c920', 'ebay')
        self.assertEqual(item.get('_key'), '94140084523.62753')
        item = monitor.get_latest_item_from_store(self.prices_data, 'headset-logitech-h600', 'ebay')
        self.assertEqual(item.get('_key'), '94140084521.30002')
        item = monitor.get_latest_item_from_store(self.prices_data, 'invalid', 'ebay')
        self.assertIs(item, None)
        item = monitor.get_latest_item_from_store(self.prices_data, 'headset-logitech-h600', 'invalid')
        self.assertIs(item, None)

    def test_is_the_cheapest_from(self):
        item = {'value': {'price': 10.00, 'product': 'webcam-logitech-c920'}}
        self.assertTrue(monitor.is_the_cheapest_from(item, self.prices_data))
        item['value']['price'] = 100
        self.assertFalse(monitor.is_the_cheapest_from(item, self.prices_data))
        item['value']['price'] = 54.99
        self.assertFalse(monitor.is_the_cheapest_from(item, self.prices_data))


if __name__ == '__main__':
    unittest.main()
