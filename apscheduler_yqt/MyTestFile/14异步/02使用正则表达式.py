#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/14 16:31
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01同步代码.py
 Description:
 Software   : PyCharm
"""
import requests
from time import time
from fake_useragent import UserAgent
import re

url = 'https://movie.douban.com/top250'


def fetch_page(url):
    response = requests.get(url,proxies={"http":None,"https":None},headers={"User-Agent":UserAgent().random})
    return response


def parse(url):
    response = fetch_page(url)
    page = response.content

    fetch_list = set()
    result = []

    for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
        result.append(title)

    for postfix in re.findall(rb'<a href="(\?start=.*?)"', page):
        fetch_list.add(url + postfix.decode())

    for url in fetch_list:
        response = fetch_page(url)
        page = response.content
        for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
            result.append(title)

    for i, title in enumerate(result, 1):
        title = title.decode()
def main():
    start = time()
    for i in range(5):
        parse(url)
    end = time()
    print ('Cost {} seconds'.format((end - start) / 5))
if __name__ == '__main__':
    main()