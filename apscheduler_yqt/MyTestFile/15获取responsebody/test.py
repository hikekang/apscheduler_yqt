#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/17 14:09
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : test.py
 Description:
 Software   : PyCharm
"""
from seleniumwire import webdriver
# from selenium import webdriver
# Import from seleniumwire

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the Google home page
driver.get('http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist')

with open('cookie.json', "r") as f:
    cookie_list = eval(f.read())
for cookie in cookie_list:
    driver.add_cookie(cookie)
print("dengdai")
driver.get('http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist')
# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        if request.url=="http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList":
            print(request.response.body)
print(driver.requests.url)

print(driver.requests.url)
for request in driver.requests:
    print(request.url)
    if request.response:
        if request.url=="http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList":
            print(request.response.body)