# -*- coding: utf-8 -*-
"""
   File Name：     getdatabyselenium
   Description :  通过selenium获取点赞、转发、评论的数量
   Author :       hike
   time：          2021/4/15 15:42
"""
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils.webdriverhelper import WebDriverHelper

class get_num_driver():
    def __init__(self):
        self.driver=WebDriverHelper.init_webdriver(is_headless=True)
    #字符串转数字
    def atoi2(s):
        s = s[::-1]
        num = 0
        for i, v in enumerate(s):
            offset = ord(v) - ord('0')
            num += offset * (10 ** i)
        return num

    #检查元素是否存在
    def is_element_present(self,browser,xpath):
        try:
            # element = browser.find_element_by_xpath("//a[contains(@node-type,'close')]")
            element = browser.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            return False
        return True



    def get_data_it(self,url):
        """
        # webdriver获取数量
        """
        self.driver.implicitly_wait(2)
        print(url)
        self.driver.get(url)
        # 向浏览器添加保存的cookies
        time.sleep(2)
        if(self.is_element_present(self.driver,"//div[@id='Pl_Official_WeiboDetail__73']")):
            print('选择数据')
            self.driver.implicitly_wait(5)
            if self.is_element_present(self.driver,"//a[contains(@node-type,'close')]"):
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@node-type,'close')]")))
                self.driver.find_element_by_xpath("//a[contains(@node-type,'close')]").click()

            zhuanfa=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[2]/a/span/span/span/em[2]').text
            pinglun=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[3]/a/span/span/span/em[2]').text
            dianzhan=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[4]/a/span/span/span/em[2]').text
            if zhuanfa == "转发":
                zhuanfa = '0'
            if pinglun=="评论":
                pinglun='0'
            if dianzhan == "赞":
                dianzhan = '0'
            print(zhuanfa,dianzhan,pinglun)
            return int(zhuanfa),int(pinglun),int(dianzhan)
        else:
            return 0,0,0
    def close(self):
        self.driver.close()
        self.driver.quit()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()