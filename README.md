Scrapy Price Monitor
====================

This is a simple price monitor built with [Scrapy](https://github.com/scrapy/scrapy)
and [Scrapy Cloud](https://scrapinghub.com/scrapy-cloud).

It is basically a Scrapy project with one spider for each online retailer that
we want to monitor prices from. In addition to the spiders, there's a Python
Script that is scheduled to run periodically on Scrapy Cloud, checking whether
the latest prices are the best ones in a given time span. If so, the monitor
sends an email alerting you about the price drops.


## Including products to monitor

There's a file `resources/urls.json` that lists the URLs from the products that
we want to monitor. If you just want to include a new product to monitor from
the retailers currently supported, just add a new key for that product and add
the URL list as its value, such as:

    {
        "headsetlogitech": [
            "https://www.amazon.com/.../B005GTO07O/",
            "http://www.bestbuy.com/.../3436118.p",
            "http://www.ebay.com/.../110985874014"
        ],
        "NewProduct": [
            "http://url.for.retailer.x",
            "http://url.for.retailer.y",
            "http://url.for.retailer.z"
        ]
    }


## Supporting further retailers

This project currently only works with 3 online retailers, and you can list them
running:

    $ scrapy list
    amazon.com
    bestbuy.com
    ebay.com

If the retailer that you want to monitor is not yet supported, just create a spider
to handle the product pages from it. To do that, run:

    $ scrapy genspider samsclub.com samsclub.com

And then, open the spider and add the extraction rules:

    $ scrapy edit samsclub.com

Have a look at the current spiders and implement the new ones using the same
structure, subclassing `BaseSpider` instead of `scrapy.Spider`.


## Customizing the Price Monitor

The price monitor sends an email using Amazon SES service, so to run it you
have to either set both `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` variables in
`price_monitor/settings.py`. If you want to use another emailing service,
you have to rewrite the `send_email_alert` function in
`price_monitor/bin/monitor.py`.

The price monitor can be further customized via parameters to the
`price_monitor/bin/monitor.py` script. We will dig on those parameters
when showing how to schedule the project on Scrapy Cloud.


## How to Deploy to Scrapy Cloud

First of all, you have to create an account on Scrapy Cloud (it's free):
https://app.scrapinghub.com/account/signup/

After that, you can to follow the steps from this video to deploy the project
into your account: https://youtu.be/JYch0zRmcgU


## How to Schedule on Scrapy Cloud

This project has two main components:

- the **spiders** that collect prices from the retailers' websites
- the **price monitor script** that checks whether there's a new deal in the latest prices

You have to schedule both the spiders and the monitor to run periodically on
Scrapy Cloud. It's a good idea to schedule all the spiders to run at the same
time and schedule the monitor to run about 15 minutes after the spiders.

Take a look at this video to learn how to schedule periodic jobs on Scrapy Cloud:
https://youtu.be/JYch0zRmcgU?t=1m51s