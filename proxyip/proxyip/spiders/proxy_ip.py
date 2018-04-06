import scrapy
from scrapy import Request
from proxyip.items import ProxyipItem

class Proxy_IP_Xici(scrapy.Spider):
    name = "Proxy_IP_Xici"

    def start_requests(self):
        base_url = "http://www.xicidaili.com/nn/{page}"
        for i in range(2):
            url = base_url.format(page=i+1)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        ip_list = response.xpath("//table[@id='ip_list']")
        tr_list = ip_list.xpath("//tr")
        for tr in tr_list[1:]:
            try:
                one = ProxyipItem()
                td_list = tr.xpath("./td")
                proxy_ip = td_list[1].xpath("text()").extract_first()
                proxy_port = td_list[2].xpath("text()").extract_first()
                proxy_country = td_list[3].xpath("./a/text()").extract_first()
                proxy_type = td_list[4].xpath("text()").extract_first()
                http_or_https = td_list[5].xpath("text()").extract_first()

                one["proxy_ip"] = http_or_https.lower()+"://"+proxy_ip
                one["proxy_port"] = int(proxy_port)
                one["proxy_country"] = proxy_country
                one["proxy_type"] = proxy_type
            except Exception:
                pass
            yield one

