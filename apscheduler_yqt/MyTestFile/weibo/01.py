#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/29 15:03
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from selenium.webdriver.chrome.webdriver import WebDriver
driver=WebDriver()
driver.get("http://www.baidu.com")
js = 'window.open("https://www.sogou.com");'
driver.execute_script(js)
driver.switch_to.window(driver.window_handles[-1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
# driver.get("http://www.baidu.com")
print("111")