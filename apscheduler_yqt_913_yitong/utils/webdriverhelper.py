# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 12:08
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : webdriverhelper.py
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium  import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

import time


# class MyWebDriver(WebDriver):
class MyWebDriver(webdriver.Chrome):
    """
    自定义WebDriver，集成一些常用功能，方便使用
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_get_url = None

    def get(self, url, wait_time=2):
        """
        默认访问链接，等待两秒
        :param url:
        :param wait_time:
        :return:
        """

        self.last_get_url = url
        super().get(url)
        time.sleep(wait_time)

    def is_url_change(self):
        """
        页面的Url是否改变了
        :return: True or False
        """
        current_url = super().current_url
        if current_url != self.last_get_url:
            return True
        else:
            return False

    def scroll_to_top(self):
        """
        滚动条拉到顶部
        :return:
        """
        js = "var scrollHeight=document.body.scrollHeight; window.scrollTo(0, 0)"
        super().execute_script(js)

    def scroll_to_bottom(self, height=None):
        """
        滚动条拉到指定位置
        :return:
        """
        if height:
            js = "var scrollHeight=document.body.scrollHeight; window.scrollTo(0, scrollHeight)"

        else:
            js = f"var scrollHeight=document.body.scrollHeight; window.scrollTo(0, {height})"

        super().execute_script(js)


class WebDriverHelper(object):
    @staticmethod
    def init_webdriver(is_headless=False, is_hide_image=False, options=None, *args, **kwargs):

        if options is None:
            options = webdriver.ChromeOptions()
            # options.add_argument("--proxy-server=http://127.0.0.1:1081")
            # options.add_argument("start-maximized");

            # options.add_argument("--window-size=1960,1080")

            options.add_argument("start-maximized")
            # options.add_argument("enable-automation")
            # options.add_experimental_option("useAutomationExtension", False)
            if is_headless:
                options.add_argument("--headless")
                options.add_argument(
                    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-browser-side-navigation")
            options.add_argument("--disable-gpu")

            # 屏蔽'保存密码'提示框
            prefs = {}
            prefs["credentials_enable_service"] = False
            prefs["profile.password_manager_enabled"] = False

            #
            # options.add_experimental_option("prefs", prefs)
            if is_hide_image:
                # 不加载图片,加快访问速度
                prefs["profile.managed_default_content_settings.images"] = 2
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["enable-automation", 'load-extension'])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument('log-level=3')
            options.add_argument("--disable-blink-features=AutomationControlled")
        _driver = MyWebDriver(options=options, *args, **kwargs)
        # _driver = webdriver.Chrome(options=options, *args, **kwargs)
        _driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        # _driver.implicitly_wait(10)
        return _driver

    @staticmethod
    def init_debug_webdriver(is_headless=False, is_hide_image=False, options=None, *args, **kwargs):

        if options is None:
            chrome_debug_port = 9999
            options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{chrome_debug_port}")

        _driver = MyWebDriver(options=options)
        _driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        wait = WebDriverWait(_driver, 5)
        # print(_driver.title)
        return _driver


# def get_track(self, distance, t):  # distance为传入的总距离，a为加速度
#      track = []
#      current = 0
#      mid = distance * t / (t + 1)
#      v = 0
#      while current < distance:
#          if current < mid:
#              a = 3
#          else:
#              a = 1
#          v0 = v
#          v = v0 + a * t
#          move = v0 * t + 1 / 2 * a * t * t
#          current += move
#          track.append(round(move))
#      return track
#
#  def move_to_gap(self, slider, tracks):
#      """
#      拖动滑块到缺口处
#      :param slider: 滑块
#      :param tracks: 轨迹
#      :return:
#      """
#      ActionChains(self.driver).click_and_hold(slider).perform()
#
#      for x in tracks:
#          print(x)
#          ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
#      time.sleep(20)
#      self.driver.refresh()
#      # ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    driver = WebDriverHelper.init_webdriver()
    driver.get("https://freeplus.tmall.com/")
    time.sleep(2)
    driver.get("http://www.baidu.com/")
    time.sleep(2)
    driver.get("https://freeplus.tmall.com/")
    # driver = WebDriverHelper.init_webdriver()
    # driver.get("https://freeplus.tmall.com/category.htm?spm=a1z10.1-b-s.w5001-14539001898.3.261d6c15VxC53p&scene=taobao_shop")
    # chrome_debug_port = 9999
    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{chrome_debug_port}")
    #
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    # wait = WebDriverWait(browser, 5)
    # print(browser.title)
    #
    # # 当前句柄
    # current_handle = browser.current_window_handle
    #
    # # browser.execute_script('window.open("https://login.taobao.com/member/login.jhtml")')
    # # browser.execute_script('window.open("http://www.baidu.com")')
    # browser.get("https://freeplus.tmall.com/")
