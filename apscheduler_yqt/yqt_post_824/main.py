#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/24 11:01
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : main.py
 Description:不使用消息队列进行接口抓取数据
 Software   : PyCharm
"""
#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
import os
import re
from concurrent.futures.thread import ThreadPoolExecutor

import pika
import asyncio
import time
import datetime
from yuqingtong import config
from utils.mylogger import logger
from selenium.webdriver.common.by import By
from utils.spider_helper import SpiderHelper
from utils.webdriverhelper import MyWebDriver
from apscheduler.triggers.cron import CronTrigger
from utils.webdriverhelper import WebDriverHelper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from utils.extract_content import extract_content as ex
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from utils import ssql_helper_test as ssql_helper
from selenium.webdriver.chrome.service import Service
from gne import GeneralNewsExtractor

extractor = GeneralNewsExtractor()
# 教程
web_url_selenium = re.compile('http[s]://(www.toutiao.com)|(mp.weixin.qq.com)|'
                              '(dy.163.com/v2/article/detail)|(kuaibao.qq.com)'
                              '|(www.sohu.com)|(www.360kuai.com)|(view.inews.qq.com)|'
                              '(tousu.sina.com.cn)|(www.chasfz.com)|(mbd.baidu.com)|'
                              '(wap.peopleapp.com)|(www.xiaohongshu.com)|'
                              '(www.laihema.com)|(kuaibao.qq.com).*')
# web_url_selenium_list=['www.toutiao.com','mp.weixin.qq.com']
video_url = re.compile('http[s]://(v.qq.com)|(live.kuaishou.com)'
                       '|(www.iesdouyin.com)|(www.ixigua.com)|(m.toutiaoimg.cn)|'
                       '(www.dongchedi.com)|(kandianshare.html5.qq.com/v2/video)|(www.dttt.net).*')


class YQTSpider(object):

    def __init__(self, myconfig, spider_driver=None, start_time=None, end_time=None, *args, **kwargs):

        if spider_driver is None:
            headless_config = eval(myconfig.getValueByDict('chromerdriver', 'is_headless'))
            self.spider_driver = WebDriverHelper.init_webdriver(is_headless=headless_config)  # type:MyWebDriver
        else:
            self.spider_driver = spider_driver  # type:MyWebDriver
        self.wait = WebDriverWait(self.spider_driver, config.WAIT_TIME)
        self.info = None
        self.myconfig = myconfig
        self.devide_keywords = False
        self.first_len = 0
        self.redis_len = 0
        # 需要替换
        # from xlsx
        # self.data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        #                                    f"data\{info['project_name']}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
        #                                    f"{self}_{info['yuqingtong_username']}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{start_time}_{end_time}.xlsx".replace(
        #                                        ':', '_'))
        # from config.ini
        self.project_name = myconfig.getValueByDict('industry_info', 'project_name')  # 项目名称
        self.industry_name = myconfig.getValueByDict('industry_info', 'industry_name')

        self.data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                           f"data\{self.project_name}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
                                           f"{self}_{self.industry_name}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{start_time}_{end_time}.xlsx".replace(
                                               ':', '_'))

        self.process_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                              "process.txt")

        # 上次终止时间
        self.last_end_time = None  # type:datetime.datetime

        # 本次终止时间
        self.next_end_time = None  # type:datetime.datetime

        # self.last_end_time = self.end_time
        default_start_time = datetime.datetime.combine(
            (datetime.datetime.now() + datetime.timedelta(days=-99)).date(),
            datetime.datetime.min.time())
        default_end_time = datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.min.time())
        self.interval = [default_start_time, default_end_time]
        self.next_page_num = 1
        self.crawl_page_count = 0  # 计数用，重启浏览器使用

    def __str__(self):
        return "舆情通"

    def _login(self, count=1, cookie_login=False):
        """
        登录
        :return: True OR False
        """
        logger.info(f"开始登录....{count}")
        driver = self.spider_driver
        if count > 10:
            logger.warning("登录次数超过10次,请检查登录流程")
            return False
        if cookie_login:
            with open('cookie.json', "r") as f:
                cookie_list = eval(f.read())
            driver.get('http://yuqing.sina.com/yqMonitor')
            for cookie in cookie_list:
                driver.add_cookie(cookie)
            driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
        else:
            driver.get("http://yuqing.sina.com/staticweb/#/login/login")
            username = driver.find_element_by_xpath("//input[@formcontrolname='userName']")
            password = driver.find_element_by_xpath("//input[@formcontrolname='password']")
            yqzcode = driver.find_element_by_xpath("//input[@formcontrolname='yqzcode']")

            submit_buttion = driver.find_element_by_xpath("//button[contains(@class,'login-form-button')]")

            # username.send_keys(self.info['yuqingtong_username'])
            username.send_keys(self.myconfig.getValueByDict('yqt_info', 'username'))
            # password.send_keys(self.info['yuqingtong_password'])
            password.send_keys(self.myconfig.getValueByDict('yqt_info', 'pwd'))

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
            code = SpiderHelper.recognise_code(code_img_base64, self.myconfig)
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
            cookies = driver.get_cookies()
            if cookie_login == False:
                with open('cookie.json', "w+") as f:
                    f.write(str(cookies))
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

    # 解析页面进行数据抓取和保存
    def _parse(self,page_data):
        """

        :param page_data:本页数据
        :return:返回解析的数据
        """
        data_list = []
        for item in page_data['data']['icontentCommonNetList']:
            data = {
                '时间': item['publishedMinute'],
                '标题': ex(item['title']) if item['title'] != None else item['title'],
                '描述': ex(item['summary']) if item['summary'] != None else item['summary'],  # 微博原创
                '链接': item['webpageUrl'],
                '转发内容': '',
                '发布人': item.get('author'),
                'comments_count': 0,
                'sort': '转发' if int(item['repostsFlg']) == 1 else '原创',
                'related_words': item['referenceKeyword'],
                'site_name': item['captureWebsiteName'],
                # 'area': item['contentAddress'],
                'area': item['province'],
                'C_Id': self.info['id']  # 客户id
            }
            r1=data['标题'].split(":")
            r2=data['标题'].split("：")
            if len(r1)>2:
                data['标题']=''.join(r1[1:])
            elif len(r2) > 2:
                data['标题'] = ''.join(r2[1:])
            if item['content'] != None:
                data['转发内容'] += (item['content'])

            if 'forwarderContent' in item.keys():
                if item['forwarderContent'] != None:
                    data['转发内容'] += (item['forwarderContent'])
                # print('forwarderContent')
            # 图像识别
            if 'ocrContents' in item.keys():
                if item['ocrContents'] != None:
                    data['转发内容'] += (item['ocrContents'])

            if item['customFlag1'] == '5':
                data['positive_prob_number'] = 0.65
            # 非敏感
            elif item['customFlag1'] == '4':
                data['positive_prob_number'] = 0.9
            # 敏感
            elif item['customFlag1'] == '2':
                data['positive_prob_number'] = 0.1
            else:
                data['positive_prob_number'] = 0.9

            data_list.append(data)
        return data_list
    def parse_data(self):
        """
        解析页面生成数据
        :return: 数据已字典形式存在list中
        """
        driver = self.spider_driver
        # i = 2
        post_data = ""
        max_page_num = self._maxpage
        for request in driver.requests:
            if request.response:
                if request.url == "http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList":
                    # i+=1
                    # if i==datacenter_id:
                    # all_data=request.response.body.decode()
                    # all_data_list.append(all_data)
                    this_all_data = request.response.body.decode().replace("true", "True").replace("false",
                                                                                                   "False").replace(
                        "null", "None")
                    this_all_data = eval(this_all_data)
                    if this_all_data['data']['maxpage'] == max_page_num:
                        if this_all_data['data']['page'] == self._currentpage:
                            print("匹配到了")
                            post_data = this_all_data
        if post_data == "":
            print("没有数据")
            return False
        else:
            print("发送")
            return self._parse(post_data)

    def _is_page_loaded(self, count=1):
        """
        判断页面时候是否加载完全
        :return:
        """
        # time.sleep(10)
        # return True
        if count > 3:
            logger.warning("页面加载可能卡住")
            return False
        try:
            # 新版
            wait_loading_disappear = self.wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, '//div[@class="spinner large"]')))
            if wait_loading_disappear:
                try:
                    wait_tr_appear = self.wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, '//tr')))
                except TimeoutException:
                    try:
                        # 本身就没数据显示没数据
                        # wait_no_data_appear = self.wait.until(
                        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.noData-word')))

                        # 新版
                        wait_no_data_appear = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, '//p[@class="ant-empty-description"]')))
                    except TimeoutException:
                        return False

            logger.info("页面加载完全")
            return True

        except TimeoutException as e:
            logger.warning(e)
            print('再次判断')
            return self._is_page_loaded(count=count + 1)

        # if count > 3:
        #     logger.warning("页面加载可能卡住")
        #     return False
        # page_source=self.spider_driver.page_source
        # if "暂无数据" in page_source:
        #     print('再次判断')
        #     return self._is_page_loaded(count=count + 1)
        # else:
        #     logger.info("页面加载完全")
        #     return True

    def filter_emoji(self,desstr, restr=u''):
        # try:
        #     co = re.compile(u'[\U00010000-\U0010ffff]')
        # except re.error:
        #     co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        return res.sub(restr, desstr)

    # 第一次根据爬取链接去重
    def quchong(self,dir_list, key):
        logger.info("第一次链接去重之前数据量为：%s", str(len(dir_list)))
        new_dirlist = []
        values = []
        for d in dir_list:
            if d[key] not in values:
                new_dirlist.append(d)
                values.append(d[key])
        return new_dirlist

    def spider_clear_data(self,data_list, clear_data_list):
        logger.info("数据处理")
        new_data_list = self.quchong(data_list, "链接")
        # 第二次滤重
        new_data_list = ssql_helper.filter_by_url(new_data_list, self.info['industry_name'])
        for data in new_data_list:
            # print(data["转发内容"])
            content = data["转发内容"]
            # 1.标题或url为空的舍去
            if data["标题"] == "" and data["链接"] == "":
                # new_data_list.remove(data)
                continue
            #     二层正文处理
            if data["标题"] == "":
                if len(data["转发内容"]) >= 20:
                    data["标题"] = content[0:20]
                else:
                    data["标题"] = content
            # 2.转发微博并且转发内容为空的舍去
            elif data["标题"] == "转发微博" and data["转发内容"] == "":
                # new_data_list.remove(data)
                print("标题为转发微博，转发内容为空")
                continue
            # 3.转发类型的微博，取前内容的前20个字符作为标题
            elif  "转发微博" in data["标题"]:
                if len(data["转发内容"]) >= 50:
                    data["标题"] = content[0:20]
                    data['描述'] = content[0:120]
                else:
                    data["标题"] = content
                    data['描述'] = content

            if data['描述'] != "" and content == "" and len(content) == 0:
                data["转发内容"] = data['描述']

            if data['转发内容'] != "" and data['描述'] == "" and len(content) != 0:
                data['描述'] = data['转发内容']



            if "微博" in data['site_name']:
                if "转发微博" in data['描述'] and content != "":
                    if len(content) >= 50:
                        data['描述'] = content[0:120]
                    else:
                        data['描述'] = content
                # print("处理标题")
                data['标题'] = data['描述'][0:20]
                if data['sort'] == '转发':
                    if len(content) >= 120:
                        data['描述'] = content[0:120]
                    else:
                        data['描述'] = content
            if len(data['描述']) > 120:
                # print("处理描述")
                data['描述'] = data['描述'][0:120]

            # 微博类型的标题进修修改
            if "weibo.com" in data["链接"] and data["sort"] != "":
                data['标题'] = data['描述'][0:20]
                if data["sort"] == "原创":
                    data['is_original'] = 1
                elif data["sort"] == "转发":
                    data['is_original'] = 0
                else:
                    data['is_original'] = 2
            else:
                data['is_original'] = 2

            data['标题'] = self.filter_emoji(data['标题'])
            data['描述'] = self.filter_emoji(data['描述'])
            data['转发内容'] = self.filter_emoji(data['转发内容'])
            data['转发内容'] = '<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;' \
                           'white-space: -pre-wrap;white-space: -o-pre-wrap; ' \
                           'word-wrap: break-word;"><zhengwen>' + data['转发内容'] + "</zhengwen></pre>"
            clear_data_list.append(data)
    def _turn_page(self, max_page_num, time_sleep):
        self.post_number = 0
        i = 0
        while 1:
            i = i + 1
            if self.crawl_page_count > config.MAX_CRAWL_PAGE_COUNT:
                self.crawl_page_count = 0
                return "restart_browser"
            if self.next_page_num > 1:
                if not self._is_page_loaded():
                    return False
            logger.info(f"当前第【{self.next_page_num}】页,共{max_page_num}页")
            self._is_page_loaded()
            time.sleep(5)
            data_list=self.parse_data()
            logger.info('数据抓取完毕')
            # 数据进行处理
            clear_data_list = []
            if data_list:
                self.spider_clear_data(data_list,clear_data_list)
            # 上传数据,每页抓取
            if clear_data_list:
                with ThreadPoolExecutor(10) as pool:
                    pool.submit(ssql_helper.upload_many_data,clear_data_list, self.industry_name, i, self.info)
                # ssql_helper.upload_many_data(clear_data_list, self.industry_name, i, self.info)
            if self.next_page_num >= 50:
                logger.info("抓取到最大页，停止")
                return True
            self.next_page_num += 1
            logger.info(f"点击下一页.....")
            if self._currentpage == self._maxpage:
                print("抓取到当前最大页面停止抓取")
                return True
            else:
                next_page = self.spider_driver.find_element_by_xpath('//li[contains(@title,"下一页")]')
                self.spider_driver.execute_script("arguments[0].click();", next_page)
            self.crawl_page_count += 1
        time.sleep(time_sleep)
        return True

    def _set_conditions(self, start_time, end_time):
        """
        设置筛选条件
        :param start_time: 起始时间
        :param end_time: 终止时间
        :return: True or Flase
        """
        driver = self.spider_driver
        if not isinstance(start_time, str):
            start_time = start_time.strftime(config.DATETIME_FORMAT)
        if not isinstance(end_time, str):
            end_time = end_time.strftime(config.DATETIME_FORMAT)
        print("选择时间")
        zidingyi = driver.find_element_by_xpath('//span[contains(text(),"自定义")]')
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", zidingyi)
        time.sleep(0.1)
        # start_input = driver.find_element_by_xpath('//input[@placeholder="开始时间"]')
        start_i = driver.find_element_by_xpath('//input[@placeholder="开始时间"]/following-sibling::span/i')
        time.sleep(0.2)
        start_i.click()
        time.sleep(0.2)
        start_input = driver.find_element_by_xpath('//div[@class="ant-calendar-date-input-wrap"]/input')
        # ant-calendar-picker-input ant-input ng-star-inserted
        time.sleep(0.2)
        start_input.clear()
        time.sleep(0.2)
        start_input.send_keys(start_time)
        time.sleep(0.2)
        start_deal_button = driver.find_element_by_xpath('//a[@class="ant-calendar-ok-btn "]')
        time.sleep(0.2)
        start_deal_button.click()
        # end_input=driver.find_element_by_xpath('//input[@placeholder="结束时间"]')
        end_i = driver.find_element_by_xpath('//input[@placeholder="结束时间"]/following-sibling::span/i')
        time.sleep(0.2)
        end_i.click()
        time.sleep(0.1)
        end_input = driver.find_element_by_xpath('//div[@class="ant-calendar-date-input-wrap"]/input')
        time.sleep(0.2)
        end_input.clear()
        time.sleep(0.2)
        end_input.send_keys(end_time)
        time.sleep(0.2)
        end_deal_button = driver.find_element_by_xpath('//a[@class="ant-calendar-ok-btn "]')
        time.sleep(0.2)
        end_deal_button.click()
        time.sleep(0.2)
        primary = driver.find_element_by_xpath('//button[@nztype="primary"]/span[contains(text(),"确认")]')
        # action = ActionChains(driver)
        # action.move_to_element(primary).perform()
        # time.sleep(0.2)
        # action.click()
        driver.execute_script("arguments[0].click();", primary)
        # primary.click()
        time.sleep(0.2)
        checkbox_list = []
        checkbox_li = self.spider_driver.find_elements_by_xpath(
            '//div[@class="monitor-info-origin rel ng-star-inserted"]//li')
        for checkbox in checkbox_li:
            tag = checkbox.text.split('\n')[0]
            checkbox_list.append({
                f"{tag}": checkbox
            })
        for key, value in eval(self.myconfig.getValueByDict("crawl_condition", "static_web_condition")).items():
            # //li[@class='ng-star-inserted']/label/span/input
            # //span[@class="ant-checkbox ant-checkbox-checked"]
            for item in checkbox_list:
                if key == list(item.keys())[0]:
                    checkbox = list(item.values())[0].find_element_by_xpath('./label/span/input')
                    break
            if value:
                if not checkbox.is_selected():
                    # action.move_to_element(checkbox[i]).perform()
                    # action.click()
                    # checkbox[i].click()
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(0.2)
            else:
                if checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(0.2)
        allinfo = self.spider_driver.find_element_by_xpath("//span[contains(text(),'全部信息')]")
        asc_time = self.spider_driver.find_element_by_xpath("//span[contains(text(),'时间升序')]")
        # allinfo.click()
        driver.execute_script("arguments[0].click();", allinfo)
        time.sleep(0.5)
        # asc_time.click()
        driver.execute_script("arguments[0].click();", asc_time)
        time.sleep(0.5)
        dingxiang_flag = eval(myconfig.getValueByDict("crawl_condition", "dingxiang"))
        if dingxiang_flag:
            source_dom = self.spider_driver.find_element_by_xpath('//a[text()=" 定向信源 "]')
            # source_dom.click()
            driver.execute_script("arguments[0].click();", source_dom)
            time.sleep(0.5)

        print("点击查询")
        self.next_page_num = 1
        find_all = driver.find_element_by_xpath("//span[text()='查询']/parent::button")
        driver.execute_script("arguments[0].click();", find_all)
        print("查询完毕")

    def _adapt_time_interval(self):
        """
        改变时间的区间
        :param start_time:
        :param end_time:
        :return: 截止时间
        """
        self.spider_driver.scroll_to_top()
        logger.info("设置时间区间...")
        """
        重新获取时间设置时间
        """
        # 设置时间
        self._set_conditions(self.last_end_time, self.next_end_time)

        if not self._is_page_loaded():
            logger.info("设置时间时页面加载出现问题")
        if not self._is_data_count_outside():  # 没有超过5000条，不用调整
            logger.info(f"小于{config.MAX_DATA_COUNT}条,符合条件")
        else:
            logger.info(f"页面数据大于{config.MAX_DATA_COUNT}条，调整时间区段")

    def _switch_data_count_perpage(self):
        #
        """
        点击每页100条按钮
        :return:
        """
        # self.spider_driver.get("http://yuqing.sina.com/newEdition/yqmonitor")
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页前，页面加载有问题")
            return False
        print("页面加载完全")
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        # if not self._is_page_loaded():
        #     logger.info("更改100条数据/每页前，页面加载有问题")
        #     return False
        time.sleep(1)
        button_js = 'document.querySelector("body > app-root > layout-default > section > ' \
                    'app-index > div > div.yqt-yqmonitor-content.p15 > app-yq-yqlist > div > ' \
                    'div.content > app-monitor-list > nz-card > div > app-info-list >' \
                    ' nz-spin > div > div > nz-table > nz-spin > div > nz-pagination >' \
                    ' ul > div > nz-select > div > div > div").click()'
        self.spider_driver.execute_script(button_js)
        # self.spider_driver.find_element_by_xpath('//div[contains(@title,"50 条/页")]/following-sibling::span').click()
        time.sleep(1)
        _200 = self.spider_driver.find_element_by_xpath('//li[contains(text(),"200 条")]')
        time.sleep(0.1)
        _200.click()
        print('选择100')
        # if not self._is_page_loaded():
        #     logger.info("更改100条数据/每页后，页面加载有问题")
        #     return False
        logger.info("更改100条数据/每页")
        return True

    def _go_page_num_by_conditions(self, is_reload=False):
        """
        根据条件和页数进入某一特定页面
        如：2020-01-01 00:00:00 至2020-01-02 00:00:00 第10页
        :return:
        """

        if is_reload:
            logger.info(f'重新进入此页面：{self.last_end_time.strftime(config.DATETIME_FORMAT)} '
                        f'- {self.next_end_time.strftime(config.DATETIME_FORMAT)} '
                        f'第{self.next_page_num}页')
            self._reload()
        # 设置时间
        self._adapt_time_interval()
        logger.info("时间和条件设置完毕")
        return True

    @property
    def _maxpage(self):
        # 获取最大页数
        page_max_num = self.spider_driver.find_element_by_xpath(
            '//li[@class="ant-pagination-simple-pager ng-star-inserted"]').get_attribute("title")
        # re.findall("\s(\d+)",page_max_num)
        # print(page_max_num[0])
        page_number = int(page_max_num.split("/")[0])
        page_max_num = int(page_max_num.split("/")[1])
        return page_max_num

    @property
    def _currentpage(self):
        # 获取当前页数
        page_max_num = self.spider_driver.find_element_by_xpath(
            '//li[@class="ant-pagination-simple-pager ng-star-inserted"]').get_attribute("title")
        # re.findall("\s(\d+)",page_max_num)
        # print(page_max_num[0])
        page_number = int(page_max_num.split("/")[0])
        page_max_num = int(page_max_num.split("/")[1])
        return page_number

    @property
    def _count_number(self):
        total_number = 0
        checkbox_list = []
        checkbox_li = self.spider_driver.find_elements_by_xpath(
            '//div[@class="monitor-info-origin rel ng-star-inserted"]//li')
        for checkbox in checkbox_li:
            tag = checkbox.text.split('\n')[0]
            number = checkbox.text.split('\n')[-1]
            checkbox_list.append({
                f"{tag}": checkbox,
                "number": 0 if number==tag  else int(number)
            })
        for item in checkbox_list[1:]:
            this_number = item['number']
            checkbox = list(item.values())[0].find_element_by_xpath('./label/span/input')
            if checkbox.is_selected():
                total_number += this_number
        return total_number

    def _is_data_count_outside(self):
        """
        数据量是否超出5000
        超出返回True
        :return:
        """
        try:
            logger.info(f"当前数据量:{self._count_number}")
            if self._count_number > config.MAX_DATA_COUNT:
                return True
        except Exception as e:
            logger.warning(e)
            return True

    def _crawl2(self, time_sleep):
        """

        :param time_sleep:
        :return:
        """
        # 首先更改为每页100条
        self._switch_data_count_perpage()

        is_reload = False
        set_conditions_reload_count = 0
        turn_page_reload_count = 0
        while 1:
            # 设置时间区间
            if not self._go_page_num_by_conditions(is_reload):
                if set_conditions_reload_count >= 3:
                    logger.warning("设置时间区间时，连续出现问题3次，退出")
                    return False
                set_conditions_reload_count += 1
                is_reload = True
                continue
            set_conditions_reload_count = 0
            time.sleep(10)
            max_page_num = self._maxpage
            print(f"最大页数：{max_page_num}")

            self.yqt_total_number = self._count_number
            if self._is_page_loaded():
                pass
            max_page_num = self._maxpage
            # --------------------------翻页并---抓取数据---------------------
            resp = self._turn_page(max_page_num, time_sleep)

            if resp == "restart_browser":
                return resp
            elif not resp:
                self._turn_page(max_page_num, time_sleep)
                if turn_page_reload_count >= 3:
                    logger.warning("翻页时，连续出现问题3次，退出")
                    return False
                turn_page_reload_count += 1
                is_reload = True
                continue
            # 翻页并抓取数据
            if resp:
                logger.info("全部抓取完毕上传数据，并进行记录")
                # 舆情通数量
                print("结束返回")
                return True

    def modifi_keywords_new(self):
        """
        关键词修改
        :return:
        """
        print("更改关键词")
        driver = self.spider_driver
        # driver.current_url
        # driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
        driver.implicitly_wait(10)
        span = driver.find_element_by_xpath('//span[@class="yqt_tree_li act ng-star-inserted"]')
        action = ActionChains(driver)
        time.sleep(1)
        # 移动到该元素
        action.move_to_element(span).perform()
        time.sleep(3)
        banzi = span.find_element_by_xpath('.//i[@class="anticon ant-dropdown-trigger"]')
        time.sleep(1)
        banzi.click()
        time.sleep(2)
        driver.find_element_by_xpath('//li[@class="ant-dropdown-menu-item ng-star-inserted"]').click()
        time.sleep(1)
        keywords = driver.find_element_by_xpath('//div[@id="senior-area"]')
        time.sleep(0.1)
        keywords.clear()
        time.sleep(0.3)
        keywords.send_keys(self.info['yqt_keywords'])
        # print(keyword)
        time.sleep(0.3)
        fitler_keywords = driver.find_element_by_xpath('//div[@id="senior-area2"]')
        time.sleep(0.3)
        fitler_keywords.clear()
        time.sleep(0.3)
        fitler_keywords.send_keys(self.excludewords)
        time.sleep(0.3)
        # 保存
        driver.find_element_by_xpath("//button[@class='mr20 ant-btn ant-btn-primary']").click()
        time.sleep(1)

    def start(self, start_time, end_time, time_sleep, info):
        # try:
        #     # 1.登录
        self.interval = [start_time, end_time]
        self.last_end_time = self.interval[0]
        self.next_end_time = self.interval[1]
        # 抓取数据
        logger.info("获取关键词")
        self.info = info
        self.keyword = info['keywords']
        self.SimultaneousWord = info['simultaneouswords']
        self.excludewords = info['excludewords']
        # 重新设置项目路径

        self.data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                           f"data\{self.project_name}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
                                           f"{self}_{self.info['customer']}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{start_time}_{end_time}.xlsx".replace(
                                               ':', '_'))
        logger.info(self.data_file_path)
        # 设置关键词
        self.modifi_keywords_new()

        # 抓取数据并记录
        resp = self._crawl2(time_sleep)
        if resp:
            logger.info("全部抓取完毕，结束")
            # pyautogui.alert("抓取完成...")

    # except Exception as e:
    #     logger.warning(e)
    # finally:
    #     print("进入finally")
    #     if self.spider_driver.service.is_connectable():
    #         print("进入finally2")
    #         self.spider_driver.quit()
    #         self.spider_driver.close()
    #         print("关闭")
    def _reload(self):
        """
        刷新页面
        :return:
        """
        self.spider_driver.refresh()
        if not self._is_page_loaded():
            return False
        return True


# 自定义时间抓取任务
def work_it(myconfig, start_time, end_time):
    # 获取驱动文件路径

    customer_list_data = ssql_helper.get_industry_keywords()

    # 根据项目进行抓取，方便统计
    # 获取行业名字
    industry_keywords = myconfig.getValueByDict('industry_info', 'industry_keywords')
    # 获取项目名字
    project_name = eval(myconfig.getValueByDict("industry_info", "project_name"))
    print(project_name)
    for d in customer_list_data:
        print(d['customer'])
        if d['industry_name'] in industry_keywords:
            if d['customer'] in project_name:
                if d['keywords'] != '':
                    time_1 = time.time()
                    yqt_spider = YQTSpider(myconfig)
                    cookie_login = eval(myconfig.getValueByDict('spider_config', 'cookie_login'))
                    # 1.登录
                    if not yqt_spider._login(cookie_login=cookie_login):
                        raise Exception("登录环节出现问题")
                    else:
                        print("loging_success")
                    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')

                    chrome_service = Service(chromedriver_path)
                    chrome_service.start()
                    yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=d)
                    print("完成一轮花费时间为：", time.time() - time_1)
                    yqt_spider.spider_driver.close()
                    chrome_service.stop()

    # if yqt_spider.spider_driver.service.is_connectable():
    #     print("进入finally2")
    #     yqt_spider.spider_driver.close()
    #     print("关闭")
    # chrome_service.stop()


def work_it_hour(myconfig):
    """
    日常抓取
    :param myconfig:
    :return:
    """
    time_info = myconfig.getDictBySection('time_info')
    # 按分钟进行抓取
    if list(time_info.keys())[0] == 'minutes':
        minutes = int(time_info['minutes'])
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time)
    # 按小时进行抓取
    elif list(time_info.keys())[0] == 'hours':
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H') + ":00:00"
        hours = int(time_info['hours'])
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H") + ":00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time)
    # 按天进行抓取
    elif list(time_info.keys())[0] == 'days':
        days = int(time_info['days'])
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig, start_time, end_time)
    # 自定义的时间
    elif list(time_info.keys())[0] == 'myself_days':
        myself_days = eval(eval(myconfig.getValueByDict('time_info', 'myself_days')))
        print(myself_days)
        print(type(myself_days))
        t_1 = myself_days[0]
        print(t_1)
        t_2 = myself_days[1]
        interval_hour = myself_days[-1] * 3600
        print(interval_hour)
        # 2021-07-15 00:00:00   1626278400
        #                       1626321600
        #                           43200

        if myself_days[-1]:
            # -----------------时间循环进行抓取-----------------
            start_int_time = int(time.mktime(time.strptime(t_1, '%Y-%m-%d %H:%M:%S')))
            end_int_time = int(time.mktime(time.strptime(t_2, '%Y-%m-%d %H:%M:%S')))
            if end_int_time - start_int_time > interval_hour:
                for i in range(start_int_time, end_int_time, interval_hour):
                    # start_time = datetime.datetime.strptime(t_1, "%Y-%m-%d %H:%M:%S")
                    start_time_pre = i
                    end_time_pre = i + interval_hour
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_pre))
                    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_pre))
                    print(start_time, end_time)
                    work_it(myconfig, start_time, end_time)
            else:
                work_it(myconfig, t_1, t_2)
        else:
            work_it(myconfig, t_1, t_2)


def work_it_one_day(myconfig, yqt_spider):
    """
    补抓前一天的数据
    从当前时刻 的前一天数据
    :param myconfig:
    :return:
    """

    now_time = int(time.time()) * 1000
    day_time_ago = now_time - 43200
    # 一天数据分成3次抓取也就是抓取的间隔时间为4小时
    for i in range(day_time_ago, now_time, 14400):
        start_time_pre = i
        end_time_pre = start_time_pre + 14400
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_pre))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_pre))
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time, yqt_spider)


def apscheduler(myconfig, yqt_spider):
    # 日常cron
    print("进来")
    cron_info = myconfig.getDictBySection('cron_info')
    print(cron_info["daily_cron"])
    trigger1 = CronTrigger.from_crontab(cron_info["daily_cron"])
    tigger_hour = CronTrigger.from_crontab(cron_info['hour_cron'])
    # 每天记录
    trigger2 = CronTrigger.from_crontab(cron_info['day_record_cron'])
    # 每日生成报表
    trigger3 = CronTrigger.from_crontab(cron_info['word_cron'])
    # 每天重新登录系统
    trigger4 = CronTrigger.from_crontab(cron_info['login_cron'])

    sched = BlockingScheduler()
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id',
                  kwargs={'myconfig': myconfig, "yqt_spider": yqt_spider})
    # 每天进行数据补抓一次
    sched.add_job(work_it_one_day, tigger_hour, max_instances=10, id='my_job_id_ever',
                  kwargs={'myconfig': myconfig, "yqt_spider": yqt_spider})
    # 进行数据统计
    sched.add_job(ssql_helper.find_day_data_count, trigger2, max_instances=10, id='my_job_id_ever_count',
                  kwargs={'myconfig': myconfig})
    # 生成报表
    sched.add_job(ssql_helper.record_day_datas, trigger3, max_instances=10, id='my_job_id_ever_record_count')
    sched.add_job(yqt_spider._login, trigger4, max_instances=10, id='my_job_id_everday_login',
                  kwargs={'cookie_login': False})
    sched.start()


def java_task():
    ab = os.path.dirname(os.path.realpath(__file__))
    path_java = os.path.join(ab, "jms-1.1.1.jar")
    # print(path_java)
    print('java程序')
    command = r'java -jar ' + path_java
    os.system(command)
    print("执行成功")


def filter_emoji(desstr, restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


if __name__ == '__main__':
    # try:
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    myconfig = config.redconfig()
    industry_name = myconfig.getValueByDict('industry_info', 'industry_name')

    # ssql_helper.get_month_data(time1, today, industry_name,flushall=True)

    # p1 = Process(target=java_task, name='java程序')
    # p2 = Process(target=apscheduler, kwargs={'myconfig': myconfig}, name='定时抓取')
    # p1.start()
    # p2.start()
    # # print("运行结束")
    work_it_hour(myconfig)
    # apscheduler(myconfig,yqt_spider)
