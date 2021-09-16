# _*_coding:utf-8 _*_
# @Time　　:2021/9/10   10:34
# @Author　 : Antipa
# @ File　　  :get_data_by_selenium.py
# @Software  :PyCharm
# @Description 通过selenium获取微博点赞转发评论数目
import time
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils.sedn_msg import send_feishu_msg
from webdriver_helper import WebDriverHelper
from lxml import etree

class get_num_driver():
    def __init__(self):
        # self.driver=WebDriverHelper.init_webdriver(is_headless=True,is_hide_image=True)
        self.driver=WebDriverHelper.init_webdriver(is_headless=False,is_hide_image=True)
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
        try:
            self.driver.implicitly_wait(20)
            print(url)
            self.driver.get(url)
            self.driver.find_element_by_xpath("//a[contains(text(),'登录')]")
            # 向浏览器添加保存的cookies
            time.sleep(2)
            print("开始抓取数据")
            print(self.driver.title)
            current_title= self.driver.title
            if  "错误" not in  current_title and "该账号行为异常" not in current_title and "随时随地" not in current_title:
                print('选择数据')
                self.driver.implicitly_wait(10)
                page_source=self.driver.page_source
                doc_html=etree.HTML(page_source)
                if self.is_element_present(self.driver,"//a[contains(@node-type,'close')]"):
                    WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@node-type,'close')]")))
                    self.driver.find_element_by_xpath("//a[contains(@node-type,'close')]").click()
                page_source = self.driver.page_source
                doc_html = etree.HTML(page_source)

                # zhuanfa=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[2]/a/span/span/span/em[2]').text
                # pinglun=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[3]/a/span/span/span/em[2]').text
                # dianzhan=self.driver.find_element_by_xpath('//div[@class="WB_handle"]/ul/li[4]/a/span/span/span/em[2]').text
                zhuanfa=doc_html.xpath('//div[@class="WB_handle"]/ul/li[2]/a/span/span/span/em[2]')[0].text
                pinglun=doc_html.xpath('//div[@class="WB_handle"]/ul/li[3]/a/span/span/span/em[2]')[0].text
                dianzan=doc_html.xpath('//div[@class="WB_handle"]/ul/li[4]/a/span/span/span/em[2]')[0].text

                if zhuanfa == "转发":
                    zhuanfa = '0'
                if pinglun=="评论":
                    pinglun='0'
                if dianzan == "赞":
                    dianzan = '0'
                print(zhuanfa,dianzan,pinglun)
                return int(zhuanfa),int(pinglun),int(dianzan)
            else:
                print("错误")
                return 0,0,0
        except Exception as e:
            send_feishu_msg(traceback.format_exc())
            return 0,0,0
    def close(self):
        self.driver.close()
        self.driver.quit()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    for i in range(20):
        print(get_num_driver().get_data_it(url="https://weibo.com/5931215633/KxdY9cCK1?type=comment"))
