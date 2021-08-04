#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/29 15:52
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : cookie_weibo.py
 Description:
 Software   : PyCharm
"""
from selenium.webdriver.chrome.webdriver import WebDriver
import time
driver=WebDriver()
driver.get("https://weibo.com/")
time.sleep(1)
cookies=driver.get_cookies()
print("cookies")