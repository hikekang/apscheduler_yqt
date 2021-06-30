# -*- coding: utf-8 -*-
"""
   File Name：     getit
   Description :
   Author :       hike
   time：          2021/4/15 15:43
"""
from selenium import webdriver
driver=webdriver.Chrome()
driver.get('https://www.weibo.com/1820571733/K9wsJF0lz?type=like')
print(driver.get_cookies())