# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    proxy_ip = scrapy.Field()
    proxy_port = scrapy.Field()
    proxy_country = scrapy.Field()
    proxy_type = scrapy.Field()
