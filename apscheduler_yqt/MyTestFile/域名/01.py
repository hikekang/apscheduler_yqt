#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/21 14:18
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import tldextract

# url = 'http://www.hike.fan-xun.com/article/infoDetail?articleID=830721&articleType=4'
# # 一级域名
# domain = tldextract.extract(url).domain
# # 二级域名
# subdomain = tldextract.extract(url).subdomain
# # 后缀
# suffix = tldextract.extract(url).suffix
# print("获取到的一级域名:{}".format(domain))
# print("获取到二级域名:{}".format(subdomain))
# print("获取到的url后缀:{}".format(suffix))


from urllib import parse
url = 'https://www.hike.google.com/spreadsheet/ccc?key=blah-blah-blah-blah#gid=1'
result = parse.urlparse(url).netloc.replace("www.","")
rx=result.split(".")
print(rx)
print('.'.join(rx))


# for i in range(0,len(rx)-1):
print('.'.join(rx[0:]))