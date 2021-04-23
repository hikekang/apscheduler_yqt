# -*- coding: utf-8 -*-
"""
   File Name：     getdatabyselenium
   Description :
   Author :       hike
   time：          2021/4/15 15:42
"""
from selenium import webdriver
from utils.ssql_helper import get_teack_datas
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chrome_options=Options()
# 无头浏览器
chrome_options.add_argument('--headless')
#
driver=webdriver.Chrome(options=chrome_options)
# driver=webdriver.Chrome()
driver.implicitly_wait(2)
driver.maximize_window()

def atoi2(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        offset = ord(v) - ord('0')
        num += offset * (10 ** i)
    return num

#检查元素是否存在
def is_element_present(browser):
    try:
        element = browser.find_element_by_xpath("//a[contains(@node-type,'close')]")
    except NoSuchElementException as e:
        return False
    return True
def get_data_it(url):
    driver.implicitly_wait(2)
    print(url)
    driver.get(url)
    # 向浏览器添加保存的cookies
    time.sleep(2)
    driver.implicitly_wait(5)
    if is_element_present(driver):
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@node-type,'close')]")))
        driver.find_element_by_xpath("//a[contains(@node-type,'close')]").click()

    zhuanfa=driver.find_element_by_xpath('//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[2]/a/span/span/span/em[2]').text
    pinglun=driver.find_element_by_xpath('//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text
    dianzhan=driver.find_element_by_xpath('//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[4]/a/span/span/span/em[2]').text
    if zhuanfa == "转发":
        zhuanfa = '0'
    if pinglun=="评论":
        pinglun='0'
    if dianzhan == "赞":
        dianzhan = '0'
    return atoi2(zhuanfa),atoi2(pinglun),atoi2(dianzhan)

url_list=get_teack_datas()
for url in url_list:
    print(type(get_data_it(url)))
