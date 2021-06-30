# -*- coding: utf-8 -*-
"""
   File Name：     1
   Description :
   Author :       hike
   time：          2021/4/21 16:28
"""
from selenium import  webdriver

driver=webdriver.Chrome()
driver.get('https://www.baidu.com/')
# driver.get("https://t.me/codeksiyon")
# 得到相应的headers
headers = driver.execute_script("var req = new XMLHttpRequest();"
                                "req.open('GET', document.location, false);"
                                "req.send(null);"
                                "return req.getAllResponseHeaders()")

# type(headers) == str

headers = headers.splitlines()

print(headers)