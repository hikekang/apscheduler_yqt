#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/3 9:49
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : ThreadPoolExecutor使用.py
 Description:
 Software   : PyCharm
"""
from concurrent.futures import ThreadPoolExecutor
import requests
from gne import  GeneralNewsExtractor
import re
from utils.webdriverhelper import WebDriverHelper

extractor=GeneralNewsExtractor()


def add_number(list:list,number:int):
    list.append(number)
    print("添加完毕")
def add_number_2(list:list,number:int):
    list.append(number)
    print("添加完毕2")
def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
def open_web(url):
    webdriver = WebDriverHelper.init_webdriver(is_headless=False, is_hide_image=True)
    js_web = 'window.open("%s");' % url
    print("打开网页")
    webdriver.implicitly_wait(10)
    webdriver.execute_script(js_web)
    import time
    time.sleep(1)
    print("切换窗口")
    webdriver.switch_to.window(webdriver.window_handles[-1])
    print("获取源码")
    page_source = webdriver.page_source
    print("关闭网页")
    print(webdriver.current_url)
    webdriver.close()
    webdriver.switch_to.window(webdriver.window_handles[0])
    print("解析数据")
    content = filter_emoji(extractor.extract(page_source, title_xpath='//html/text()')['content'])
    print(content)
def test_print(list_1):
    for item in list_1:
        print(item)

if __name__ == '__main__':
    test_list = []
    list_2=[12,3,4,5,6,7,9]
    with ThreadPoolExecutor(5) as pool:
        # # for i in range(10):
        # # url=f"https://v.qq.com/channel/variety?listpage={i+1}&channel=variety&source=1&exclusive=1"
        # url="https://www.toutiao.com/w/i1703710959904775/"
        # pool.submit(open_web,url)
        # for i in range(10):
        #     pool.submit(add_number,test_list,i)
        #     pool.submit(add_number_2,test_list,i)
        pool.submit(test_print,list_2)