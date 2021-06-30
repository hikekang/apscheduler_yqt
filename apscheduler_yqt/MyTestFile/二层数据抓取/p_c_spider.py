# -*- coding: utf-8 -*-
"""
   File Name：     p_c_spider
   Description :
   Author :       hike
   time：          2021/4/28 13:41
"""
import queue
import time
import requests
from fake_useragent import UserAgent
import concurrent.futures
import time
def second_craw(url):
    print(url)
    pass

def second_parse(html):
    return html

urls=[]
for i in range(10):
    urls.append(i)
time.sleep(1)
with concurrent.futures.ThreadPoolExecutor() as pool:
    htmls=pool.map(second_craw,urls)

print("craw over")

with concurrent.futures.ThreadPoolExecutor() as pool:
    futures=[]
    for html in htmls:
        future=pool.submit(second_parse,html)
        da=future
        futures.append(da)

    for url in futures:
        print(url.result())

    # for future in concurrent.futures.as_completed(futures):

