import random

import requests
import time
from imgspider import config

last_proxy = None

def get_proxy():
    if random.random() <= 0.1:
        return None
    while True:
        j = requests.get("http://127.0.0.1:5010/get/").json()
        if j.get('fail_count') == 0:
            return j.get('proxy')
        interval = config.get_proxy_interval
        if config.random_interval:
            interval *= random.random() * 2
        time.sleep(interval)


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get(*args, **kwargs):
    global last_proxy
    retry_cnt = config.retry_num
    resp = None
    while retry_cnt > 0:
        proxy = get_proxy()
        if last_proxy == proxy:
            interval = config.crawl_interval
            if config.random_interval:
                interval *= random.random() * 2
            time.sleep(interval)
        try:
            if proxy is None:
                resp = requests.get(*args, **kwargs)
            else:
                resp = requests.get(*args, proxies={"http": "http://{}".format(proxy)}, **kwargs)
                delete_proxy(proxy)

            last_proxy = proxy
            break
        except Exception as e:
            print(e)
            delete_proxy(proxy)
            retry_cnt -= 1
    return resp
