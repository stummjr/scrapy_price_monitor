# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {'price_monitor': ['resources/*.json']},
    entry_points = {'scrapy': ['settings = price_monitor.settings']},
)
