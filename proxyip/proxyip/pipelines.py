# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import treq
from proxyip.settings import Proxy_API
import json
import requests
#
# def print_response(response):
#     print(response.code)


class ProxyipPipeline(object):
    def process_item(self, item, spider):
        # d = treq.post(Proxy_API, dict(item))
        # d.addCallback(print_response)
        req = requests.post(Proxy_API, data=dict(item))
        print(req.status_code)
        return item
