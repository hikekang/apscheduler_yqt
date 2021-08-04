#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/31 11:39
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from gne import GeneralNewsExtractor
import requests
from fake_useragent import UserAgent
url='https://finance.sina.com.cn/tech/2021-07-20/doc-ikqcfnca7823444.shtml'
url='https://zhuanlan.zhihu.com/p/377248898'
header={
    'User-Agent':UserAgent().random
}

html=requests.get(url,headers=header)
print(html.content.decode('utf-8'))
extractor=GeneralNewsExtractor()
content=extractor.extract(html.content.decode('utf-8'),title_xpath='//html/text()')['content']
print(content)