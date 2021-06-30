#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/15 15:58
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 评论.py
 Description:
 Software   : PyCharm
"""
import requests, re, json, pandas as pd, time, random
from selenium import webdriver  # selenium===2.48.0 (支持phantomjs)
from lxml import etree
from openpyxl import load_workbook

page_url = "https://weibo.com/2803301701/I2nLRFwQZ?type=comment#_rnd1623741686910"
browser = webdriver.Chrome()
browser.get(page_url)
# wb_text = browser.find_element_by_class_name('WB_feed_repeat S_bg1 WB_feed_repeat_v3')
time.sleep(5)
for i in range(2):  # 窗口下拉
    # x管水平，y管垂直

    js = 'window.scrollTo(0,%s)' % (i * 100)
    browser.execute_script(js)
    time.sleep(0.1)
    tree = etree.HTML(browser.page_source)  # //*[@id="Pl_Official_WeiboDetail__58"]/div/div/div/div[4]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/text()
    print(tree)
    book_list = tree.xpath('//div[@class="WB_text"]/text()')  # 选一个标签作为树根，
    print(book_list)
