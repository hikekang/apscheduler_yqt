#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 16:15
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : domain.py
 Description:
 Software   : PyCharm
"""
import re
from urllib.parse import urlparse


class ExtractLevelDomain():

    def __init__(self):
        self.topHostPostfix = [
            '.com', '.la', '.io',
            '.co', '.cn', '.info',
            '.net', '.org', '.me',
            '.mobi', '.us', '.biz',
            '.xxx', '.ca', '.co.jp',
            '.com.cn', '.net.cn', '.org.cn',
            '.mx', '.tv', '.ws',
            '.ag', '.com.ag', '.net.ag',
            '.org.ag', '.am', '.asia',
            '.at', '.be', '.com.br',
            '.net.br',
            '.name',
            '.live',
            '.news',
            '.bz',
            '.tech',
            '.pub',
            '.wang',
            '.space',
            '.top',
            '.xin',
            '.social',
            '.date',
            '.site',
            '.red',
            '.studio',
            '.link',
            '.online',
            '.help',
            '.kr',
            '.club',
            '.com.bz',
            '.net.bz',
            '.cc',
            '.band',
            '.market',
            '.com.co',
            '.net.co',
            '.nom.co',
            '.lawyer',
            '.de',
            '.es',
            '.com.es',
            '.nom.es',
            '.org.es',
            '.eu',
            '.wiki',
            '.design',
            '.software',
            '.fm',
            '.fr',
            '.gs',
            '.in',
            '.co.in',
            '.firm.in',
            '.gen.in',
            '.ind.in',
            '.net.in',
            '.org.in',
            '.it',
            '.jobs',
            '.jp',
            '.ms',
            '.com.mx',
            '.nl', '.nu', '.co.nz', '.net.nz',
            '.org.nz',
            '.se',
            '.tc',
            '.tk',
            '.tw',
            '.com.tw',
            '.idv.tw',
            '.org.tw',
            '.hk',
            '.co.uk',
            '.me.uk',
            '.org.uk',
            '.vg']

        self.extractPattern = r'[\.](' + '|'.join([h.replace('.', r'\.') for h in self.topHostPostfix]) + ')$'
        self.pattern = re.compile(self.extractPattern, re.IGNORECASE)
        self.level = "*"

    def parse_url(self, url):
        parts = urlparse(url)
        host = parts.netloc
        m = self.pattern.search(host)
        return m.group() if m else host

    def parse_url_level(self, url, level="*"):
        extractRule = self._parse_regex(level)
        parts = urlparse(url)
        host = parts.netloc
        pattern = re.compile(extractRule, re.IGNORECASE)
        m = pattern.search(host)
        self.level = level
        return m.group() if m else host

    def set_level(self, level):
        extractRule = self._parse_regex(level)
        self.extractPattern = extractRule
        self.pattern = re.compile(self.extractPattern, re.IGNORECASE)
        self.level = level

    def add_top_domain(self, top):
        if not top.startswith('.'):
            raise ValueError('top_domain must have . (.com|.com.cn|.net)')
        if top not in self.topHostPostfix:
            self.topHostPostfix.append(top)
            self._reset()
            return True
        else:
            return False

    def _reset(self):
        self.set_level(self.level)

    def _parse_regex(self, level):
        # extractRule = r'([\W]|[\w]*\.?)%s(' + '|'.join([h.replace('.', r'\.') for h in self.topHostPostfix]) + ')$'
        extractRule = r'(\w*\.?)%s(' + '|'.join([h.replace('.', r'\.') for h in self.topHostPostfix]) + ')$'
        level = level if level == "*" else "{%s}" % level
        extractRule = extractRule % (level)
        return extractRule


if __name__ == "__main__":
    filter = ExtractLevelDomain()
    url="https://www.bilibili.com/read/cv11834173"
    url='https://www.hike.haidong.cn'
    for i in range(3,0,-1):
        print(i)
        domain_level=filter.parse_url_level(url, level=i).replace("www.","")
        print(domain_level)
    # parts = urlparse(url)
    # print(parts.netloc.split('.'))

    # for i in range(1,4):
    #     if i==2:
    #         break
    #     print("hike")
    # import  redis

    # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    # r = redis.Redis(connection_pool=pool)
    # print(r.hexists("url",'weibo.com'))
    # ret = eval(r.hget("url", domain_level))
    # print(ret)