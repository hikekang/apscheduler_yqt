#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/12 17:17
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01pagesouce.py
 Description:
 Software   : PyCharm
"""
### 生产者
import pika
import time
import datetime
import os
import sys
import threading
from multiprocessing.dummy import Pool as ThreadPool
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# ab=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# path_utils=os.path.join(ab,'utils')
# sys.path.append(path_utils)
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from utils.mylogger import logger
from utils.spider_helper import SpiderHelper
# from utils.ssql_helper import get_industry_keywords

from utils.ssql_helper_test import get_industry_keywords
from utils.extract_content import extract_content as ex
from utils.webdriverhelper import MyWebDriver
from utils.webdriverhelper import WebDriverHelper
from yuqingtong import config
# from utils import  ssql_helper
# from utils import qinbaobing_ssql as ssql_helper
from utils import ssql_helper_test as ssql_helper
import re
from selenium.webdriver.chrome.service import Service
from multiprocessing import Process
# from utils.email_helper import my_Email
from lxml import etree
from utils.post_helper import SecondData
from concurrent.futures import ThreadPoolExecutor
import json
from utils.secodnd_data_utils import crawl_second_by_requests,crawl_second_by_webdriver
from gne import GeneralNewsExtractor
import requests
extractor=GeneralNewsExtractor()
# 教程
web_url_selenium=re.compile('http[s]://(www.toutiao.com)|(mp.weixin.qq.com)|'
                            '(dy.163.com/v2/article/detail)|(kuaibao.qq.com)'
                            '|(www.sohu.com)|(www.360kuai.com)|(view.inews.qq.com)|'
                            '(tousu.sina.com.cn)|(www.chasfz.com)|(mbd.baidu.com)|'
                            '(wap.peopleapp.com)|(www.xiaohongshu.com)|'
                            '(www.laihema.com)|(kuaibao.qq.com).*')
# web_url_selenium_list=['www.toutiao.com','mp.weixin.qq.com']
video_url=re.compile('http[s]://(v.qq.com)|(live.kuaishou.com)'
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

    def _login(self, count=1,cookie_login=False):
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
            driver.get('http://yuqing.sina.com/yqMonitor')
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
            cookies=driver.get_cookies()
            if cookie_login==False:
                with open('cookie.json',"w+") as f:
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
    def parse_data(self,datacenter_id):
        """
        解析页面生成数据
        :return: 数据已字典形式存在list中
        """
        driver = self.spider_driver
        xpath_data={
            "page_source":driver.page_source,
            "info":self.info,
            "datacenter_id":datacenter_id
        }
        channel.basic_publish(exchange='',
                              routing_key='xpath',
                              body=str(xpath_data))
        print("发送")
    # 数据处理
    # def clear_data(self, data_list,clear_data_list):
    def _is_page_loaded(self, count=1):
        """
        判断页面时候是否加载完全
        :return:
        """
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


    def _turn_page(self, max_page_num, time_sleep):
        self.post_number = 0
        i=0
        while 1:
            i=i+1
            if self.crawl_page_count > config.MAX_CRAWL_PAGE_COUNT:
                self.crawl_page_count = 0
                return "restart_browser"
            if self.next_page_num > 1:
                if not self._is_page_loaded():
                    return False
            # print("页面加载完成")

            logger.info(f"当前第【{self.next_page_num}】页,共{max_page_num}页")
            self.parse_data(i)
            logger.info('数据抓取完毕')
            # 数据进行处理
            # 上传数据,每页抓取
            if self.next_page_num >= 50:
                logger.info("抓取到最大页，停止")
                data_count = int(self.spider_driver.find_element_by_css_selector(
                    'span[ng-bind="originStat.total"]').text)
                break
            self.next_page_num += 1
            logger.info(f"点击下一页.....")
            try:
                self.spider_driver.find_element_by_xpath('//i[contains(@ng-click,"gotoPage2(page + 1)")]').click()
            except NoSuchElementException:
                logger.info("没有找到下一页的按钮")
                break
            self.crawl_page_count += 1
        #
        # with ThreadPoolExecutor(3) as pool:
        #     for i in range(1,max_page_num+1):
        #         pool.submit(craw,i+1)
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
        driver.find_element_by_xpath('//span[contains(text(),"自定义")]/parent::div').click()
        time.sleep(0.1)
        start_input = driver.find_element_by_xpath('//input[@id="startTimeInput1"]')
        # ant-calendar-picker-input ant-input ng-star-inserted
        time.sleep(0.2)
        start_input.clear()
        time.sleep(0.2)
        start_input.send_keys(start_time)
        time.sleep(0.2)
        end_input=driver.find_element_by_xpath('//input[@id="endTimeInput1"]')
        time.sleep(0.1)
        end_input.clear()
        time.sleep(0.2)
        end_input.send_keys(end_time)
        time.sleep(0.2)
        # condai
        driver.find_element_by_xpath('//span[contains(@ng-click,"confirmTime(1)")]').click()

        for key,value in eval(self.myconfig.getValueByDict("crawl_condition","condition")).items():
            if key=="all" and value:
                time.sleep(0.2)
                input=self.spider_driver.find_element_by_xpath(f"//input[@id='{key}']")
                if not input.is_selected():
                    input.click()
            elif key!="all":
                if value:
                    time.sleep(0.2)
                    input = self.spider_driver.find_element_by_xpath(f"//input[@id='{key}']")
                    if not input.is_selected():
                        input.click()
                else:
                    time.sleep(0.2)
                    input = self.spider_driver.find_element_by_xpath(f"//input[@id='{key}']")
                    if input.is_selected():
                        input.click()
        allinfo=self.spider_driver.find_element_by_xpath("//span[contains(text(),'全部信息')]")
        asc_time=self.spider_driver.find_element_by_xpath("//span[contains(text(),'时间升序')]")
        allinfo.click()
        time.sleep(0.5)
        asc_time.click()
        time.sleep(0.5)
        print("点击查询")
        driver.find_element_by_xpath("//a[@id='searchListButton']").click()
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
        logger.info(f"页面数据大于{config.MAX_DATA_COUNT}条，调整时间区段")


    def _switch_data_count_perpage(self):
        #
        """
        点击每页100条按钮
        :return:
        """
        self.spider_driver.get("http://yuqing.sina.com/newEdition/yqmonitor")
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页前，页面加载有问题")
            return False
        print("页面加载完全")
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页前，页面加载有问题")
            return False
        self.spider_driver.find_element_by_xpath('//button[@title="50条/页"]').click()
        time.sleep(1)
        self.spider_driver.find_element_by_xpath('//span[contains(text(),"100条/页")]').click()
        print('选择100')
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页后，页面加载有问题")
            return False
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
        page_max_num = int(self.spider_driver.find_element_by_xpath('//span[@ng-bind="maxpage"]').text)
        print(page_max_num)
        return page_max_num

    @property
    def _count_number(self):
        total_number=0
        for key,value in eval(self.myconfig.getValueByDict("crawl_condition","condition")).items():
            if key=="all" and value:
                total_number=int(self.spider_driver.find_element_by_xpath('//span[@ng-bind="originStat.total"]').text)
            elif key!="all" and value :
                total_number+=int(self.spider_driver.find_element_by_xpath(f'//input[@id="{key}"]/parent::div/following-sibling::div[1]/span').text)
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
            max_page_num = self._maxpage
            print(f"最大页数：{max_page_num}")

            self.yqt_total_number=self._count_number
            if self._is_page_loaded():
                max_page_num = self._maxpage
                # 翻页并抓取数据
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
                    yqt_count = self.yqt_total_number
                    # 记录文件的路径
                    record_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                    f"record\{self.project_name}", f"{self}_记录.xlsx")
                    # 本次抓取TS_A库和QBBB_B库、中的数量
                    sql_number_A,sql_number_B = ssql_helper.find_curent_num(self.interval[0],
                                                                            self.interval[1],
                                                                            self.myconfig,
                                                                            self.info,
                                                                            yqt_count)
                    time.sleep(1)
                    # myconfig=config.redconfig()
                    # 需要增加一个B库中的数量
                    data_list = [self.project_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 self.last_end_time, self.next_end_time]
                    # 本地记录文件保存
                    # SpiderHelper.save_record_auto(record_file_path, yqt_count, self.post_number, sql_number_A,sql_number_B,
                    #                               data_list=data_list)
                    record_day_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                    f"record\{self.project_name}", f"{self}_{self.project_name}记录.xlsx")
                    # SpiderHelper.save_record_day_data(record_day_file_path, yqt_count, sql_number_B)
                    # my_Email().send_xlsx(record_file_path)
                    # record_dict = (self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.last_end_time,
                    # self.next_end_time, yqt_count, self.post_number, self.project_name)

                    record_dict = (
                        self.industry_name,  # 行业名称
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 抓取时间
                        self.last_end_time,  # 开始时间
                        self.next_end_time,  # 结束时间
                        yqt_count,  # 舆情通数量
                        self.post_number,  # 上传数量
                        self.info['customer'],  # 项目名称
                        self.first_len,  # 第一次过滤之后的数量
                        self.redis_len,  # redis过滤之后的数量
                        sql_number_A,
                        sql_number_B
                    )

                    # 数据统计记录
                    ssql_helper.record_log(record_dict)
                    # SpiderHelper.save_record(record_file_path,yqt_count,xlsx_num,
                    # post_info['number'],post_info2['number'],sql_number,data_list=data_list)
                    print("结束返回")
                    return True
            else:
                return False
    def modifi_keywords_new(self):
        """
        关键词修改
        :return:
        """
        print("更改关键词")
        driver = self.spider_driver
        # driver.current_url
        driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
        driver.implicitly_wait(10)
        span = driver.find_element_by_xpath('//span[@class="yqt_tree_li act ng-star-inserted"]')
        action = ActionChains(driver)
        time.sleep(1)
        # 移动到该元素
        action.move_to_element(span).perform()
        time.sleep(3)
        banzi = span.find_element_by_xpath('.//i[@class="anticon ant-dropdown-trigger"]')
        banzi.click()
        time.sleep(2)
        driver.find_element_by_xpath('//li[@class="ant-dropdown-menu-item ng-star-inserted"]').click()
        time.sleep(1)
        keywords = driver.find_element_by_xpath('//div[@id="senior-area"]')
        keywords.clear()
        keywords.clear()
        time.sleep(0.3)
        keywords.send_keys(self.info['yqt_keywords'])
        # print(keyword)
        time.sleep(0.3)
        fitler_keywords = driver.find_element_by_xpath('//div[@id="senior-area2"]')
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
def work_it(myconfig, start_time, end_time,yqt_spider):
    # 获取驱动文件路径

    customer_list_data = ssql_helper.get_industry_keywords()


    # 根据项目进行抓取，方便统计
    # 获取行业名字
    industry_keywords=myconfig.getValueByDict('industry_info','industry_keywords')
    # 获取项目名字
    project_name=eval(myconfig.getValueByDict("industry_info", "project_name"))
    print(project_name)
    for d in customer_list_data:
        print(d['customer'])
        if d['industry_name'] in industry_keywords:
            if d['customer'] in project_name:
                if d['keywords']!='':
                    time_1=time.time()
                    yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=d)
                    print("完成一轮花费时间为：",time.time()-time_1)

    # if yqt_spider.spider_driver.service.is_connectable():
    #     print("进入finally2")
    #     yqt_spider.spider_driver.close()
    #     print("关闭")
    # chrome_service.stop()


def work_it_hour(myconfig,yqt_spider):
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
        work_it(myconfig, start_time, end_time,yqt_spider)
    # 按小时进行抓取
    elif list(time_info.keys())[0] == 'hours':
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H') + ":00:00"
        hours = int(time_info['hours'])
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H") + ":00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time,yqt_spider)
    #按天进行抓取
    elif list(time_info.keys())[0] == 'days':
        days = int(time_info['days'])
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig, start_time, end_time,yqt_spider)
    # 自定义的时间
    elif list(time_info.keys())[0] == 'myself_days':
        myself_days=eval(eval(myconfig.getValueByDict('time_info','myself_days')))
        print(myself_days)
        print(type(myself_days))
        t_1=myself_days[0]
        print(t_1)
        t_2=myself_days[1]
        interval_hour=myself_days[-1]*3600
        print(interval_hour)
        # 2021-07-15 00:00:00   1626278400
        #                       1626321600
        #                           43200

        if myself_days[-1]:
            # -----------------时间循环进行抓取-----------------
            start_int_time=int(time.mktime(time.strptime(t_1,'%Y-%m-%d %H:%M:%S')))
            end_int_time=int(time.mktime(time.strptime(t_2,'%Y-%m-%d %H:%M:%S')))
            if end_int_time-start_int_time>interval_hour:
                for i in range(start_int_time,end_int_time,interval_hour):
                    # start_time = datetime.datetime.strptime(t_1, "%Y-%m-%d %H:%M:%S")
                    start_time_pre = i
                    end_time_pre=i+interval_hour
                    start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_pre))
                    end_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_pre))
                    print(start_time,end_time)
                    work_it(myconfig, start_time, end_time,yqt_spider)
            else:
                work_it(myconfig,t_1,t_2,yqt_spider)
        else:
            work_it(myconfig,t_1, t_2,yqt_spider)


def work_it_one_day(myconfig,yqt_spider):
    """
    补抓前一天的数据
    从当前时刻 的前一天数据
    :param myconfig:
    :return:
    """

    now_time=int(time.time())*1000
    day_time_ago=now_time-43200
    # 一天数据分成3次抓取也就是抓取的间隔时间为4小时
    for i in range(day_time_ago,now_time,14400):
        start_time_pre=i
        end_time_pre=start_time_pre+14400
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_pre))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_pre))
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time,yqt_spider)


def apscheduler(myconfig,yqt_spider):
    # 日常cron
    print("进来")
    cron_info = myconfig.getDictBySection('cron_info')
    print(cron_info["daily_cron"])
    trigger1 = CronTrigger.from_crontab(cron_info["daily_cron"])
    tigger_hour = CronTrigger.from_crontab(cron_info['hour_cron'])
    # 每天记录
    trigger2 = CronTrigger.from_crontab(cron_info['day_record_cron'])
    trigger3 = CronTrigger.from_crontab(cron_info['word_cron'])

    trigger4 = CronTrigger.from_crontab(cron_info['login_cron'])

    sched = BlockingScheduler()
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id', kwargs={'myconfig': myconfig,"yqt_spider":yqt_spider})
    # 每天进行数据补抓一次
    sched.add_job(work_it_one_day, tigger_hour, max_instances=10, id='my_job_id_ever', kwargs={'myconfig': myconfig,"yqt_spider":yqt_spider})
    # 进行数据从统计
    sched.add_job(ssql_helper.find_day_data_count, trigger2, max_instances=10, id='my_job_id_ever_count',
                  kwargs={'myconfig': myconfig})
    sched.add_job(ssql_helper.record_day_datas, trigger3, max_instances=10, id='my_job_id_ever_record_count')
    sched.add_job(yqt_spider._login, trigger4, max_instances=10, id='my_job_id_everday_login')
    sched.start()


def java_task():
    ab = os.path.dirname(os.path.realpath(__file__))
    path_java = os.path.join(ab, "jms-1.1.1.jar")
    # print(path_java)
    print('java程序')
    command = r'java -jar ' + path_java
    os.system(command)
    print("执行成功")
def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

if __name__ == '__main__':
    credentials=pika.PlainCredentials('admin','admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1',port=5672,virtual_host='/',credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='xpath',durable=True)
    # try:
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    myconfig = config.redconfig()
    industry_name = myconfig.getValueByDict('industry_info', 'industry_name')

    ssql_helper.get_month_data(time1, today, industry_name,flushall=True)

    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')

    chrome_service = Service(chromedriver_path)
    chrome_service.start()
    yqt_spider = YQTSpider(myconfig)
    cookie_login = eval(myconfig.getValueByDict('spider_config', 'cookie_login'))
    # 1.登录
    if not yqt_spider._login(cookie_login=cookie_login):
        raise Exception("登录环节出现问题")
    else:
        print("loging_success")
    # p1 = Process(target=java_task, name='java程序')
    # p2 = Process(target=apscheduler, kwargs={'myconfig': myconfig}, name='定时抓取')
    # p1.start()
    # p2.start()
    # # print("运行结束")
    work_it_hour(myconfig,yqt_spider)
    # apscheduler(myconfig,yqt_spider)



