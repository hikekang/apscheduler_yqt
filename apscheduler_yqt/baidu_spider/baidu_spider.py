# -*- coding: utf-8 -*-
"""
   File Name：     baidu_spider
   Description :
   Author :       hike
   time：          2021/4/20 13:19
"""
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup

from fake_useragent import UserAgent
t1= int(time.time())
t2=t1-36000
url='http://www.baidu.com/s?ie=utf-8' \
    '&f=8&rsv_bp=1&tn=baidu&wd=%s&oq=%s' \
    '&rsv_pq=a9636e1e00055dd6' \
    '&rsv_t=2a70VgAdo4ldyiXmlT8IdiuR5uvnM0wZTPL+ieA7FXQ6vCY1UwCboVYZ1mQ' \
    '&rqlang=cn' \
    '&rsv_enter=1' \
    '&rsv_dl=tb' \
    '&gpc=stf=%d,%d|stftype=1' \
    '&tfflag=1'%('优速','优速',t2,t1)
print(url)
headers={
    'User-Agent':UserAgent().random
}
# url='http://www.baidu.com/s?ie=UTF-8&wd=优速'
# print(url)
r=requests.get(url)
# print(r.text)
# html=etree.HTML(r.text,etree.HTMLParser())
html=etree.HTML(r.text)
# print(etree.tostring(html,encoding='utf-8').decode('utf-8'))
print(html.xpath('//div[@class="result-op c-container new-pmd xpath-log"]'))
divs_list=html.xpath('//div[@class="result c-container new-pmd"]')
print(divs_list)
for div in divs_list:
    a = div.xpath('.h3/a')
    print()