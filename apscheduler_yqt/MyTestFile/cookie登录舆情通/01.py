#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/29 13:41
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from selenium.webdriver.chrome.webdriver import WebDriver
import time
driver=WebDriver()
cookie_list=[{
        'domain': 'yuqing.sina.com',
        # 'expiry': int(time.time()),
        'httpOnly': True,
        'name': 'WS_KEY',
        'path': '/',
        'secure': False,
        'value': 'a8613b961847e70671376e4ba6832f2d'
    }, {
        'domain': 'yuqing.sina.com',
        # 'expiry': int(time.time()),
        'httpOnly': True,
        'name': 'www',
        'path': '/',
        'secure': False,
        'value': 'userSId_yqt365_itit01_933298_15482'
    }
]
# with open('cookie.json','w') as f:
#     f.write(str(cookie_list))
driver.get('http://yuqing.sina.com/yqMonitor')
for cookie in cookie_list:
    driver.add_cookie(cookie)
# driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
# for cookie in cookie_list:
#     driver.add_cookie(cookie)
# print("11")
# print("11")
# print("11")
# cookie_ll=[]
# import json
# with open('cookie.json','r') as f:
#     data=f.read()
#     print(data)
#     print(type(data))
#     cookie_ll=eval(data)
# 
# print(type(cookie_ll))
# for cookie in cookie_ll:
#     cookie.pop('expiry')

# for cookie in cookie_ll:
#     print(cookie)

# driver.get('http://yuqing.sina.com/yqMonitor')
#
# for cookie in cookie_ll:
#     print(cookie)
#     print(type(cookie))
#     driver.add_cookie(cookie)
# driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
# for cookie in cookie_list:
#     driver.add_cookie(cookie)