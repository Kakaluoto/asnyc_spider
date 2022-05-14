# coding=utf-8
import requests
from fake_useragent import UserAgent
from pprint import pprint
import random


class ProxyPool:
    ip_test_url = 'http://httpbin.org/get'

    def __init__(self, port=5010):
        self.port = port

    def get_proxy(self):
        http_url = "http://127.0.0.1:{}/get/?type=http".format(self.port)
        http_proxy = requests.get(http_url).json().get("proxy")
        https_url = "http://127.0.0.1:{}/get/?type=https".format(self.port)
        https_proxy = requests.get(https_url).json().get("proxy")
        return {"http": "http://{}".format(http_proxy), "https": "https://{}".format(https_proxy)}

    def all_proxy(self, https_filter=False):
        if not https_filter:
            url = "http://127.0.0.1:{}/all/".format(self.port)
            proxies = requests.get(url).json()
            proxies = [{"http": "http://{}".format(proxy["proxy"])} for proxy in proxies]
            return proxies
        else:
            http_url = "http://127.0.0.1:{}/all/?type=http".format(self.port)
            http_proxies = requests.get(http_url).json()
            http_proxies = [proxy.get("proxy") for proxy in http_proxies]

            https_url = "http://127.0.0.1:{}/all/?type=https".format(self.port)
            https_proxies = requests.get(https_url).json()
            https_proxies = [proxy.get("proxy") for proxy in https_proxies]
            return {"http_list": http_proxies, "https_list": https_proxies}

    def count_proxy(self):
        url = "http://127.0.0.1:{}/count/".format(self.port)
        return requests.get(url).json()

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:{}/delete/?proxy={}".format(self.port, proxy))

    def get_useful_ip(self):
        ip_list = self.all_proxy()
        for proxy_ip in ip_list:
            try:
                # 设置超时时间，如果代理不能使用则切换下一个
                headers = {'User-Agent': UserAgent(use_cache_server=False).random}
                result = requests.get(url=self.ip_test_url, headers=headers,
                                      proxies=proxy_ip, timeout=5)
                print("%s is available,kept." % proxy_ip)
            except Exception as e:
                # 此代理ip不能用，从列表中移除
                ip_list.remove(proxy_ip)
                self.delete_proxy(proxy=proxy_ip["http"].split("/")[-1])
                print("%s is unavailable,removed." % proxy_ip)
                continue
        return ip_list


if __name__ == "__main__":
    proxypool = ProxyPool()
    proxies = proxypool.get_useful_ip()
    proxy = random.choice(proxies)
    headers = {'User-Agent': UserAgent(use_cache_server=False).random, "Connection": "close"}
    img_url = "http://image.baidu.com/search/flip?tn=baiduimage&word=%E9%87%91%E6%9E%AA%E9%B1%BC&pn=0"
    baidu_url = "http://www.baidu.com"
    result = requests.get(url=img_url, headers=headers,
                          proxies=proxy, timeout=5, verify=False)
    result.encoding = "utf-8"
    pprint(result.text)

