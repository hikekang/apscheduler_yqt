# -*- coding: utf-8 -*-
"""
   File Name：     webdriver_test
   Description :
   Author :       hike
   time：          2021/5/6 14:22
"""
"""
彻底结束chrome进程
"""
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
chrome_service=Service('D:\Anacadon\envs\python36\chromedriver.exe')
chrome_service.start()
driver=WebDriver()
driver.get("http://www.baidu.com")
import time
time.sleep(10)
driver.quit()
chrome_service.stop()