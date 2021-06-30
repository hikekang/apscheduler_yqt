#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/18 1:34
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : 01.py
# @Software: PyCharm
from selenium import webdriver
from browsermobproxy import Server

from selenium.webdriver.chrome.options import Options


def _login(self, count=1):
    """
    登录
    :return: True OR False
    """
    driver = self.spider_driver
    if count > 10:
        return False

    driver.get("http://yuqing.sina.com/staticweb/#/login/login")
    username = driver.find_element_by_xpath("//input[@formcontrolname='userName']")
    password = driver.find_element_by_xpath("//input[@formcontrolname='password']")
    yqzcode = driver.find_element_by_xpath("//input[@formcontrolname='yqzcode']")

    submit_buttion = driver.find_element_by_xpath("//button[contains(@class,'login-form-button')]")

    # username.send_keys(self.info['yuqingtong_username'])
    username.send_keys(self.info.getValueByDict('yqt_info', 'username'))
    # password.send_keys(self.info['yuqingtong_password'])
    password.send_keys(self.info.getValueByDict('yqt_info', 'pwd'))

    logger.info("获取验证码....")
    while 1:
        code_img = None
        try:
            code_img = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'validate/image')]")))
        except TimeoutException:
            pass

        if code_img and code_img.size.get("width") > 0:
            break
        logger.info("验证码图片没加载出来，刷新...")
        driver.refresh()
    code_img_base64 = code_img.screenshot_as_base64
    code = SpiderHelper.recognise_code(code_img_base64, self.info)
    logger.info(f"获取验证码:{code}")
    if not code:
        code = "1234hi"

    yqzcode.send_keys(code)
    time.sleep(0.2)
    submit_buttion.click()

    try:
        wait = self.wait.until(
            EC.invisibility_of_element_located((By.XPATH, "//input[@formcontrolname='userName']")))
        print(wait)
        print("登录成功")
        return True
    except Exception as e:
        logger.warning(e)

    try:
        mobile_code = driver.find_element_by_css_selector(".ant-modal-content .mt20 input")
        # pyautogui.prompt("需要手机验证")
        while not driver.is_url_change():
            print("还没填写验证码")
            time.sleep(1)

    except NoSuchElementException:
        pass

    if driver.is_url_change():
        print("登录成功")
        return True
    else:
        return self._login(count=count + 1)

server = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))

driver = webdriver.Chrome(chrome_options=chrome_options)

base_url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=selenium%20%20%E6%8D%95%E6%8D%89network&oq=selenium%25E8%258E%25B7%25E5%258F%2596%25E8%25AF%25B7%25E6%25B1%2582%25E5%25A4%25B4&rsv_pq=b4e22f8000526b99&rsv_t=61f2VftYRV8IgXFmN1sKOP%2FFjhtNmAuC5IuWmnF%2BhKjeRQBjjxy2nL4C144&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_btype=t&inputT=5657&rsv_sug3=31&rsv_sug1=19&rsv_sug7=100&rsv_sug2=0&rsv_sug4=5957"
proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
driver.get(base_url)


result = proxy.har

for entry in result['log']['entries']:
    _url = entry['request']['url']
    # 根据URL找到数据接口
    if "/api/v2/aweme/post" in _url:
        _response = entry['response']
        _content = _response['content']['text']
        # 获取接口返回内容
        print(_content)

server.stop()
driver.quit()
