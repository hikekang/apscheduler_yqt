# _*_coding:utf-8 _*_
# @Time　　:2021/9/10   13:22
# @Author　 : Antipa
# @ File　　  :webdriver_helper.py
# @Software  :PyCharm
# @Description
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

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