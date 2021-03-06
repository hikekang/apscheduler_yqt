#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/20 11:28
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : old_apscheduler_yqt.py
 Description:
 Software   : PyCharm
"""
# -*- coding: utf-8 -*-
"""
   File Name：     apscheduler_yqt
   Description :
   Author :       hike
   time：          2021/4/18 9:47
"""
# -*- coding=utf-8 -*-
import time
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
ab = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
path_utils = os.path.join(ab, 'utils')
sys.path.append(path_utils)
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pyquery import PyQuery as pq
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

from utils.webdriverhelper import MyWebDriver
from utils.my_pyautogui import pyautogui
from utils.webdriverhelper import WebDriverHelper
from yuqingtong import config
# from utils import  ssql_helper
from utils import ssql_helper_test as ssql_helper
import re
from selenium.webdriver.chrome.service import Service
from multiprocessing import Process
from utils.email_helper import my_Email


class YQTSpider(object):

    def __init__(self, info, spider_driver=None, start_time=None, end_time=None, *args, **kwargs):
        if spider_driver is None:
            self.spider_driver = WebDriverHelper.init_webdriver(is_headless=config.HEAD_LESS)  # type:MyWebDriver
        else:
            self.spider_driver = spider_driver  # type:MyWebDriver
        self.wait = WebDriverWait(self.spider_driver, config.WAIT_TIME)
        self.info = info
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
        self.project_name = info.getValueByDict('industry_info', 'project_name')
        self.industry_name = info.getValueByDict('industry_info', 'industry_name')

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

    def _login(self, count=1):
        """
        登录
        :return: True OR False
        """
        driver = self.spider_driver
        if count > 10:
            logger.warning("登录次数超过10次,请检查登录流程")
            return False

        logger.info(f"开始登录....{count}")
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

    # 解析页面进行数据抓取和保存
    def _parse(self, page_source):
        doc = pq(page_source)
        keywords_id = doc.find('span.site-menu-title.ml15.tippy:first-child').attr('id').split('_')[-1]
        items = doc.find('tbody tr.ng-scope').items()

        data_list = []
        for item in items:
            td_title = item.find('td:nth-child(2)')
            td_origins = item.find('td:nth-child(4)')
            td_time = item.find('td:last-child')

            # print(td_time)

            def parse_time(td_time):
                from datetime import datetime
                ymd_1 = td_time.find('span:first-child').text()
                ymd_2 = td_time.find('span:last-child').text()
                try:
                    if "年" in ymd_1:  # 不是今年的数据
                        ymd = "".join([ymd_1, ymd_2])
                    elif "今天" in ymd_2:  # 今天的数据
                        ymd = " ".join([f"{str(datetime.now().date())}", ymd_1])
                        return datetime.strptime(ymd, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        ymd = " ".join([f"{datetime.now().year}年" + ymd_2, ymd_1])
                    return datetime.strptime(ymd, "%Y年%m月%d日 %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    logger.warning(e)
                    logger.warning(td_time)

            # 转发类型  原创
            sort = td_title.find('div.news-item-tools.font-size-0 span.tag-yuan').text()
            # 转发内容
            repost_content = td_title.find('div.item-title.resend-news-item-title').text().replace('\n', '')
            pinglun = td_title.find('div.inline-block.mr10.tag-ping').text().replace('\n', '')  # 评论

            if repost_content:
                sort = "转发"
            if pinglun:
                sort = "评论"
            # 微博原创类型的内容、转发类型的评论内容、其他类型的内容
            content = td_title.find('div.item-title.news-item-title.contenttext.ng-binding').text().replace('\n', ''),

            title = td_title.find('span[ng-bind-html="icc.title | trustAsHtml"]').text().replace('\n', '')
            site_name = td_origins.find('span[ng-bind="icc.captureWebsiteName"]').text()

            if (site_name == '新浪微博' or site_name == '今日头条'):
                data = {
                    '时间': parse_time(td_time),
                    '标题': content[0].replace("'", ""),
                    '描述': content[0].replace("'", ""),  # 微博原创
                    '链接': td_title.find('.news-item-tools.font-size-0 div:nth-child(2)>div>ul>li:nth-child(4) a').attr(
                        "href"),
                    '转发内容': repost_content.replace("'", ""),
                    # '发布人': td_title.find('a[ng-click="getDetail(icc,cucurrrentKeyword);"]').text(),
                    '发布人': td_title.find('div.profile-title.inline-block>a').text(),
                    'ic_id': td_title.find('a[ng-click="getDetail(icc,rentKeyword);"]').attr('value'),
                    'keywords_id': keywords_id,
                    'attitude': td_title.find(
                        'div[ng-show="view.resultPresent != 3"] div.sensitive-status-content:not(.ng-hide)>span:first-child').text(),
                    'images': ",".join([img.attr('src') for img in item.find('.actizPicShow img').items()]),
                    'reposts_count': item.find(
                        'div.news-item-title.color-gray-6.font-size-12.ng-scope span:first>span').text(),

                    'comments_count': item.find(
                        'div.news-item-title.color-gray-6.font-size-12.ng-scope span:nth-child(3)>span').text(),
                    'sort': sort,

                    'industry': td_title.find(
                        '.news-item-tools.font-size-0 div:nth-child(1) div[ng-if="secondTrade!=null"]').text(),

                    'related_words': td_title.find(
                        '.news-item-tools.font-size-0 div:nth-child(1) span[ng-bind="icc.referenceKeyword"]').text(),

                    'site_name': td_origins.find('span[ng-bind="icc.captureWebsiteName"]').text(),
                    # 'area': td_origins.find('div[ng-bind="icc.province"]').text(),
                    'area': td_title.find('div[ng-bind="icc.contentAddress"]').text(),

                }
                # 针对微博而言
                if sort == '评论':
                    data['链接'] = td_title.find(
                        '.news-item-tools.font-size-0 div:nth-child(2)>div>ul>li:nth-child(3) a').attr("href")
                    # 评论的内容
                    biaoti = td_title.find('div.item-title.news-item-title.dot.ng-binding').text().replace('\n',
                                                                                                           '').replace(
                        "'", "")
                    data['标题'] = biaoti
                    data['发布人'] = td_title.find('a[ng-if="icc.commentAuthor != null"]').text()
                    data['描述'] = biaoti
                elif sort == '原创':
                    data['转发内容'] = data['描述']
                if len(data['标题']) > 20:
                    data['标题'] = data['标题'][0:20]
            else:
                data = {
                    '时间': parse_time(td_time),
                    '标题': title.replace("'", ""),
                    '描述': content[0].replace("'", "").replace("\n", ""),
                    '链接': td_title.find('.news-item-tools.font-size-0 div:nth-child(2)>div>ul>li:nth-child(4) a').attr(
                        "href"),
                    '转发内容': repost_content.replace("'", "").replace("\n", ""),
                    # '发布人': td_title.find('div[class="profile-title inline-block"]>a>span:first-child').text(),
                    '发布人': td_title.find('a[ng-click="getDetail(icc,currentKeyword);"]>span:first-child').text(),
                    'ic_id': td_title.find('a[ng-click="getDetail(icc,currentKeyword);"]').attr('value'),
                    'keywords_id': keywords_id,
                    'attitude': td_title.find(
                        'div[ng-show="view.resultPresent != 3"] div.sensitive-status-content:not(.ng-hide)>span:first-child').text(),
                    'images': ",".join([img.attr('src') for img in item.find('.actizPicShow img').items()]),
                    'reposts_count': item.find(
                        'div.news-item-title.color-gray-6.font-size-12.ng-scope span:first>span').text(),

                    'comments_count': item.find(
                        'div.news-item-title.color-gray-6.font-size-12.ng-scope span:nth-child(3)>span').text(),

                    'sort': sort,

                    'industry': td_title.find(
                        '.news-item-tools.font-size-0 div:nth-child(1) div[ng-if="secondTrade!=null"]').text(),

                    'related_words': td_title.find(
                        '.news-item-tools.font-size-0 div:nth-child(1) span[ng-bind="icc.referenceKeyword"]').text(),

                    'site_name': td_origins.find('span[ng-bind="icc.captureWebsiteName"]').text(),
                    'area': td_title.find('div[ng-bind="icc.contentAddress"]').text(),

                }

                # print(data)
                #     publish_man = re.sub(':|：', '', data['发布人'])
                #     data['发布人'] = publish_man
                #     if(len(data['发布人'])>10):
                #         data['发布人']=''
                #
                if '：' in data['发布人'] or ":" in data['发布人']:
                    publish_man = re.sub(':|：', '', data['发布人'])
                    # publish_man=data['发布人'].split(":")[0]
                    data['发布人'] = publish_man
                else:
                    if (len(data['发布人']) > 10):
                        data['发布人'] = ''
            if (len(data['发布人']) > 15):
                data['发布人'] = ''
            positive_prob = td_title.find(
                'div.sensitive-status-wrapper.p-r>div.sensitive-status-content:not(.ng-hide)>span:first-child').text()
            positive_dict = {
                "敏感": 0.1,
                "非敏感": 0.9,
                "中性": 0.5
            }
            data['positive_prob_number'] = positive_dict[positive_prob.split()[0]]
            data_list.append(data)
        return data_list

    # 数据处理
    def clear_data(self, data_list):
        logger.info("数据处理")
        t1 = time.time()
        new_data_list = self.quchong(data_list, "链接")

        # 第二次滤重
        new_data_list = ssql_helper.filter_by_url(new_data_list, self.industry_name)
        self.redis_len += len(new_data_list)
        sec_list = []
        for data in new_data_list:
            # 1.标题或url为空的舍去
            if data["标题"] == "" and data["链接"] == "":
                # new_data_list.remove(data)
                continue
            if data["标题"] == "":
                if len(data["转发内容"]) >= 20:
                    data["标题"] = data["转发内容"][0:20]
                else:
                    data["标题"] = data["转发内容"]
            #     2.转发微博并且转发内容为空的使舍去
            elif data["标题"] == "转发微博" and data["转发内容"] == "":
                # new_data_list.remove(data)
                print("标题为转发微博，转发内容为空")
                continue
            #     3.转发类型的微博，取前内容的前20个字符作为标题
            elif data["标题"] == "转发微博":
                if len(data["转发内容"]) >= 20:
                    data["标题"] = data["转发内容"][0:20]
                else:
                    data["标题"] = data["转发内容"]
                data['描述'] = data["转发内容"]

            if data['描述'] != "" and data["转发内容"] == "" and len(data["转发内容"]) == 0:
                data["转发内容"] = data['描述']

            if data['转发内容'] != "" and data['描述'] == "" and len(data['转发内容']) != 0:
                data['描述'] = data['转发内容']

            if "weibo.com" in data["链接"] and data["sort"] != "":
                if data["sort"] == "原创":
                    data['is_original'] = 1
                elif data["sort"] == "转发":
                    data['is_original'] = 0
                else:
                    data['is_original'] = 2
            else:
                data['is_original'] = 2
            sec_list.append(data)
        t2 = time.time()
        print("花费时间:", t2 - t1)
        print('数据处理完毕')
        print("数据处理完毕之后的数量", len(sec_list))
        return sec_list

    # 第一次根据爬取链接去重
    def quchong(self, dir_list, key):
        print("第一次链接去重")
        print(len(dir_list))
        new_dirlist = []
        values = []
        for d in dir_list:
            if d[key] not in values:
                new_dirlist.append(d)
                values.append(d[key])

        print("第一次滤重之后的数量:", self.first_len)
        self.first_len += len(new_dirlist)
        return new_dirlist

    def parse_data(self):
        """
        解析页面生成数据
        :return: 数据已字典形式存在list中
        """
        driver = self.spider_driver
        page_source = driver.page_source
        return self._parse(page_source)

    def _set_conditions(self, start_time, end_time):
        """
        设置筛选条件
        :param start_time: 起始时间
        :param end_time: 终止时间
        :return: True or Flase
        """
        driver = self.spider_driver
        start_time_str = start_time.strftime(config.DATETIME_FORMAT)
        end_time_str = end_time.strftime(config.DATETIME_FORMAT)
        driver.find_element_by_css_selector('div.inline-block.custom-time-period').click()

        start_input = driver.find_element_by_css_selector("#startTimeInput1")
        start_input.clear()
        start_input.send_keys(start_time_str)
        time.sleep(0.2)
        end_input = driver.find_element_by_css_selector("#endTimeInput1")
        end_input.clear()
        end_input.send_keys(end_time_str)
        time.sleep(0.2)
        driver.find_element_by_css_selector('span[ng-click="confirmTime(1)"]').click()
        time.sleep(0.2)
        # -----------点击全部------------------
        # driver.find_element_by_css_selector('#informationContentType0').click()
        # time.sleep(0.2)
        # driver.find_element_by_css_selector('#select0').click()
        # time.sleep(0.2)
        # ------------------------------------
        driver.find_element_by_css_selector("#searchListButton").click()
        # time.sleep(2)
        return True

    # 细化时间，分开爬取
    def _adapt_time_interval(self):
        """
        改变时间的区间
        :param start_time:
        :param end_time:
        :return: 截止时间
        """
        # end_time = datetime.datetime.now()
        # start_time = end_time + datetime.timedelta(days=-30)

        while 1:
            self.spider_driver.scroll_to_top()
            logger.info("设置时间区间...")
            self._save_process()
            # self._set_conditions(start_time, end_time)
            # self.modifi_keywords()

            """
            重新获取时间设置时间

            """
            # 设置时间
            self._set_conditions(self.last_end_time, self.next_end_time)

            if not self._is_page_loaded():
                logger.info("设置时间时页面加载出现问题")
                return False
                if not self._is_data_count_outside():  # 没有超过5000条，不用调整
                    logger.info(f"小于{config.MAX_DATA_COUNT}条,符合条件")
                break
            logger.info(f"页面数据大于{config.MAX_DATA_COUNT}条，调整时间区段")
            # 超出5000条进行分词抓取
            # return False
            self.devide_keywords = True
            break

            # ---------------------------------------------------------------------------------------------------------
            # 超出5000条进行时间设置

            # 停止时间划分
            # timedelta = self.next_end_time - self.last_end_time
            # if timedelta.days <= 1:
            #     timedelta_hours = timedelta.total_seconds() / 60 / 60
            #     if timedelta_hours <= 1:
            #         logger.info("时间区间小于一小时，无法调整")
            #         break
            #     logger.info("时间区间小于一天，继续细化调整")
            #     # 下次开始时间
            #     self.next_end_time = self.last_end_time + datetime.timedelta(hours=timedelta_hours / 2)
            # else:
            #     # return None
            #     self.next_end_time = datetime.datetime.combine(self.last_end_time.date(),
            #                                                    datetime.datetime.min.time()) + \
            #                          datetime.timedelta(days=round(timedelta.days / 2))

            # # ---------------------------------------------------------------------------------------------------------
            # if timedelta.days % 2 == 0:  # 偶数
            #     end_time = start_time.date() + datetime.timedelta(days=timedelta.days / 2)
            # else:
            #     end_time = start_time.date() + datetime.timedelta(days=(timedelta.days + 1) / 2)
            # ---------------------------------------------------------------------------------------------------------
        logger.info(
            f"当前时间区间:{self.last_end_time.strftime(config.DATETIME_FORMAT)}  --"
            f" {self.next_end_time.strftime(config.DATETIME_FORMAT)}")

    @property
    def _maxpage(self):
        # 获取最大页数
        return int(self.spider_driver.find_element_by_css_selector('span.page-number-total.ng-binding').text)

    @property
    def _count_number(self):
        return int(self.spider_driver.find_element_by_css_selector('span[ng-bind="originStat.total"]').text)

    def _is_data_count_outside(self):
        """
        数据量是否超出5000
        超出返回True
        :return:
        """
        try:
            data_count = int(self.spider_driver.find_element_by_css_selector(
                'span[ng-bind="originStat.total"]').text)
            logger.info(f"当前数据量:{data_count}")
            if data_count > config.MAX_DATA_COUNT:
                return True
        except Exception as e:
            logger.warning(e)
            return True

    def _is_page_loaded(self, count=1):
        """
        判断页面时候是否加载完全
        :return:
        """
        if count > 3:
            logger.warning("页面加载可能卡住")
            return False
        try:
            # 加载数据时的圆圈消失就说明页面加载完全
            # logger.debug(f"检测是否加载完全。。{count}")
            # loading_ico = self.spider_driver.find_element_by_css_selector('#iccListLoading .spinner').is_displayed()
            # print(loading_ico)
            wait_data_count_loading_disappear = self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '#originStatId>.spinner')))

            wait_loading_disappear = self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '#iccListLoading>.spinner')))
            if wait_loading_disappear:
                try:
                    wait_tr_appear = self.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody.contenttext>tr')))
                except TimeoutException:
                    try:
                        # 本身就没数据显示没数据
                        wait_no_data_appear = self.wait.until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.noData-word')))
                    except TimeoutException:
                        return False

            logger.info("页面加载完全")
            return True

        except TimeoutException as e:
            logger.warning(e)
            print('再次判断')
            return self._is_page_loaded(count=count + 1)

    # 100条
    def _switch_data_count_perpage(self):
        """
        点击每页100条按钮
        :return:
        """
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页前，页面加载有问题")
            return False

        self.spider_driver.scroll_to_bottom(10000)
        time.sleep(1)
        self.spider_driver.find_element_by_css_selector('div[ng-show="selectType == 1"]').click()
        time.sleep(1)
        self.spider_driver.find_element_by_css_selector(
            'div[ng-show="selectType == 1"] li[data-original-index="2"]>a').click()
        print('选择100')
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页后，页面加载有问题")
            return False
        logger.info("更改100条数据/每页")
        return True

    def _reload(self):
        """
        刷新页面
        :return:
        """
        self.spider_driver.refresh()
        self.spider_driver.refresh()
        if not self._is_page_loaded():
            return False
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
        # else:
        # logger.info(f'进入此页面：{self.condition.get("start_time").strftime(config.DATETIME_FORMAT)} '
        #             f'- {self.condition.get("end_time").strftime(config.DATETIME_FORMAT)} ')

        # 细化时间
        self._adapt_time_interval()

        if self.next_page_num > 1:
            logger.info(f"直接进入第{self.next_page_num}页")
            self.spider_driver.find_element_by_css_selector('input[ng-model="goPage"]').send_keys(
                self.next_page_num)
            time.sleep(0.5)
            self.spider_driver.find_element_by_css_selector('div[ng-click="gotoSearchList();"]').click()
        if not self._is_page_loaded():
            logger.info("直接进入第多少页时页面加载出现问题")
            return False
        page_num = self.spider_driver.find_element_by_css_selector("#listPage").text
        if int(page_num) != self.next_page_num:
            logger.warning("页面上当前页面和应该进入的页面不一样，请检查")
            return False
        logger.info("进入成功")
        return True

    def _save_process(self):
        with open(self.process_file_path, "w", encoding="utf-8") as f:
            f.write(f"{self.interval[0]}至{self.interval[1]}|"
                    f"{self.last_end_time}_{self.next_end_time}_{self.next_page_num}_{self.data_file_path}")

    def _turn_page(self, max_page_num, time_sleep):
        """
        翻页
        :return:
        """
        self.post_number = 0
        # 翻页开始
        while 1:
            if self.crawl_page_count > config.MAX_CRAWL_PAGE_COUNT:
                self.crawl_page_count = 0
                return "restart_browser"
            # todo:每解析完一页数据，就保存下当前任务进程到文件中：时间区间，第几页,保存文件路径
            # self._save_process()
            if self.next_page_num > 1:
                if not self._is_page_loaded():
                    return False
            # print("页面加载完成")

            logger.info(f"当前第【{self.next_page_num}】页,共{max_page_num}页")
            data_list = self.parse_data()
            logger.info('数据抓取完毕')
            # 数据进行处理
            data_list = self.clear_data(data_list)

            # 插入到数据库，返回一个成功插入的值
            # 上传数据
            if data_list:
                ssql_helper.upload_many_data(data_list, self.industry_name)

            logger.info(f"解析到{len(data_list)}条数据")
            self.post_number += len(data_list)
            # SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path,sheet_name=self.info['sheet_name'])
            SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path, sheet_name=self.industry_name)
            logger.info(f"保存完毕")

            # 想要抓取的最大页数，可以修改
            if self.next_page_num >= 50:
                logger.info("抓取到最大页，停止")
                data_count = int(self.spider_driver.find_element_by_css_selector(
                    'span[ng-bind="originStat.total"]').text)

                break
            self.next_page_num += 1
            logger.info(f"点击下一页.....")
            self._save_process()
            try:
                self.spider_driver.find_element_by_xpath('//i[@class="fa-page-arrow-right ng-scope"]').click()
            except NoSuchElementException:
                logger.info("没有找到下一页的按钮")
                break
            self.crawl_page_count += 1

        time.sleep(time_sleep)
        return True

    def _crawl2(self, time_sleep):
        # 记录任务时间区
        logger.info(
            f'任务时间区间：{self.interval[0]} --- '
            f'{self.interval[1]}')

        # 改成每页100条
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

            ret = self.keyword.split("|")
            keywords = []
            for i in range(0, len(ret), 3):
                key = ''
                for j in ret[i:i + 3]:
                    key += j + '|'
                keywords.append(key)
            # 多关键词抓取
            if self._count_number > 5000:
                for keyword in keywords:
                    input_keywords = self.spider_driver.find_element_by_xpath('//input[@ng-model="view.secondKeyword"]')
                    input_keywords.clear()
                    input_keywords.send_keys(keyword)
                    time.sleep(1)
                    self.spider_driver.find_element_by_xpath('//a[@ng-click="searchListButton();"]').click()
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
                        turn_page_reload_count = 0
                        # 翻页结束

                        # 设置下次抓取条件
                        self.next_page_num = 1
                        if self.next_end_time >= self.interval[1]:
                            logger.info("解析到终止时间，抓取完成")
                            logger.info("全部抓取完毕上传数据")
                            logger.info("开始记录")
                            # 舆情通数量
                            yqt_count = self._count_number
                            record_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            f"record\{self.project_name}", f"{self}_记录.xlsx")
                            sql_number = ssql_helper.find_info_count(self.interval[0], self.interval[1],
                                                                     self.industry_name)
                            data_list = [self.project_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         self.last_end_time, self.next_end_time]
                            SpiderHelper.save_record_auto(record_file_path, yqt_count, self.post_number, sql_number,
                                                          data_list=data_list)
                            # record_dict = (self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.last_end_time,
                            # self.next_end_time, yqt_count, self.post_number, self.project_name)
                            record_dict = (self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                           self.last_end_time,
                                           self.next_end_time, yqt_count, self.post_number, self.project_name,
                                           self.first_len, self.redis_len)
                            print(record_file_path)
                            ssql_helper.record_log(record_dict)
                            # SpiderHelper.save_record(record_file_path,yqt_count,xlsx_num,post_info['number'],post_info2['number'],sql_number,data_list=data_list)
                            return True
                        else:
                            self.last_end_time = self.next_end_time  # 上次终止时间就是下次起始时间
                            self.next_end_time = self.interval[1]
            else:
                if self._is_page_loaded():
                    max_page_num = self._maxpage
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
                    turn_page_reload_count = 0
                    # 翻页结束

                    # 设置下次抓取条件
                    self.next_page_num = 1
                    if self.next_end_time >= self.interval[1]:
                        logger.info("解析到终止时间，抓取完成")
                        logger.info("全部抓取完毕上传数据")
                        logger.info("开始记录")
                        # 舆情通数量
                        yqt_count = self._count_number
                        record_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                        f"record\{self.project_name}", f"{self}_记录.xlsx")
                        sql_number = ssql_helper.find_info_count(self.interval[0], self.interval[1],
                                                                 self.industry_name)
                        data_list = [self.project_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     self.last_end_time, self.next_end_time]
                        # 本地文件记录数量
                        SpiderHelper.save_record_auto(record_file_path, yqt_count, self.post_number, sql_number,
                                                      data_list=data_list)
                        # record_dict = (self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.last_end_time,
                        # self.next_end_time, yqt_count, self.post_number, self.project_name)
                        record_dict = (
                            self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            self.last_end_time,
                            self.next_end_time, yqt_count, self.post_number, self.project_name, self.first_len,
                            self.redis_len)
                        # print(record_dict)
                        ssql_helper.record_log(record_dict)
                        # SpiderHelper.save_record(record_file_path,yqt_count,xlsx_num,post_info['number'],post_info2['number'],sql_number,data_list=data_list)
                        return True
                    else:
                        self.last_end_time = self.next_end_time  # 上次终止时间就是下次起始时间
                        self.next_end_time = self.interval[1]

    def _load_condition_process_file(self):
        if os.path.exists(self.process_file_path):
            print(self.process_file_path)
            with open(self.process_file_path, "r", encoding="utf-8") as f:
                last_task_process = f.readline()
            return last_task_process

    # 关键词修改
    def modifi_keywords(self):
        """
        读取config。xlsx文件关键词
        根据关键词进行修改
        """
        driver = self.spider_driver
        print("返回旧版本")
        old_yqt=driver.find_element_by_xpath('//div[@class="yqt-header-mnlogin2"]')
        time.sleep(1)
        old_yqt.click()
        time.sleep(4)
        print("点击")
        li = driver.find_element_by_xpath('//li[contains(@id,"kw_li_")]')
        span = li.find_element_by_xpath('//span[@class="fa-tree-plan-tools-bar"]')
        action = ActionChains(driver)
        time.sleep(1)
        action.move_to_element(li).perform()
        time.sleep(3)
        span.click()
        time.sleep(2)
        driver.find_element_by_xpath('//li[@class="add-plan-trigger"]/a').click()
        time.sleep(1)
        keywords = driver.find_element_by_xpath('//div[@class="edit_textarea mb5 ng-binding"]')
        keywords.clear()
        time.sleep(0.3)
        keywords.send_keys(self.keyword)
        time.sleep(0.3)

        # 保存
        driver.find_element_by_id("saveHighSetKeyword").click()
        time.sleep(1)

    def start(self, start_time, end_time, time_sleep, info, is_one_day):
        try:
            # 1.登录
            if not self._login():
                raise Exception("登录环节出现问题")
            self.interval = [start_time, end_time]
            self.last_end_time = self.interval[0]
            self.next_end_time = self.interval[1]
            # 抓取数据
            print("获取关键词")
            self.info = info
            # 重新设置项目路径

            self.data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                               f"data\{self.project_name}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
                                               f"{self}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{start_time}_{end_time}.xlsx".replace(
                                                   ':', '_'))
            print(self.data_file_path)
            self.keyword = info['keywords']
            self.SimultaneousWord = info['simultaneouswords']
            self.excludewords = info['excludewords']
            # 设置关键词
            self.modifi_keywords()
            if is_one_day == False:
                pass
                # -------------再次设置时间（定时抓取）----------------
                # end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # start_time = (datetime.datetime.now() - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
                # start_time1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                # end_time1 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                #
                # self.interval = [start_time1, end_time1]
                # self.last_end_time = self.interval[0]
                # self.next_end_time = self.interval[1]
                # -----------定时抓取时间设置完毕----------------------

            # 抓取数据并记录
            resp = self._crawl2(time_sleep)

            if resp == "restart_browser":
                logger.info("重启浏览器")
                self.spider_driver.quit()
                self.spider_driver = WebDriverHelper.init_webdriver(is_headless=config.HEAD_LESS)
                self.wait = WebDriverWait(self.spider_driver, config.WAIT_TIME)
                self.start(resp, self.info, self.last_end_time, self.next_end_time)
            elif resp is True:
                os.remove(self.process_file_path)
            # pyautogui.alert("抓取完成...")
        except Exception as e:
            my_e = my_Email()
            my_e.send_message(str(e), self.industry_name)
            logger.warning(e)
        finally:
            if self.spider_driver.service.is_connectable():
                self.spider_driver.quit()


# 修改xlsx文件进行自动抓取
def xlsx_work():
    time_list = config.get_time_list()
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time1 = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    # ssql_helper.get_month_data(time1, today)
    # print(time_list)
    infos = config.row_list
    yqt_spider = YQTSpider(infos[0])
    data = get_industry_keywords()
    project_list = ssql_helper.merger_industry_data(data)[1]
    for tim in time_list:
        yqt_spider.start(start_time=tim['start_time'], end_time=tim['end_time'], time_sleep=tim['time_delay'],
                         infos=project_list)


# 自定义时间抓取任务
def work_it(myconfig, start_time, end_time):
    # 获取项目信息
    # from xlsx
    infos = config.row_list
    # from config.ini

    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')
    chrome_service = Service(chromedriver_path)
    chrome_service.start()

    # yqt_spider = YQTSpider(infos[0], start_time=start_time, end_time=end_time)
    yqt_spider = YQTSpider(myconfig, start_time=start_time, end_time=end_time)

    p_data = []
    project_list_1 = ssql_helper.get_industry_keywords()
    project_list = ssql_helper.merger_industry_data(project_list_1)
    for project_data in project_list:
        # if project_data['industry_name'] == '流通贸易':
        if project_data['industry_name'] == yqt_spider.industry_name:
            p_data.append(project_data)
    print(p_data)
    yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=p_data[0], is_one_day=False)
    chrome_service.stop()


def work_it_hour():
    myconfig = config.redconfig()

    # end_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + "00:00:00"
    time_info = myconfig.getDictBySection('time_info')
    if list(time_info.keys())[0] == 'minutes':
        minutes = int(time_info['minutes'])
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig, start_time, end_time)
    elif list(time_info.keys())[0] == 'hours':
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H') + ":00:00"
        hours = int(time_info['hours'])
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H") + ":00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time)
    else:
        pass


def work_it_one_day():
    myconfig = config.redconfig()
    time_info = myconfig.getDictBySection('time_info')
    if list(time_info.keys())[0] == 'days':
        days = int(time_info['days'])
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig,start_time, end_time)
    else:
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig,start_time, end_time)


def apscheduler():
    trigger1 = CronTrigger(hour='0-23', minute='01', second=00, jitter=5)
    trigger2 = CronTrigger(hour='0', minute='01', second=00, jitter=5)
    sched = BlockingScheduler()
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id')
    sched.add_job(work_it_one_day, trigger2, max_instances=10, id='my_job_id_ever')
    sched.start()


def java_task():
    ab = os.path.dirname(os.path.realpath(__file__))
    path_java = os.path.join(ab, "jms-1.1.1.jar")
    # print(path_java)
    command = r'java -jar ' + path_java
    os.system(command)
    print("执行成功")


if __name__ == '__main__':
    # today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # time1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    # ssql_helper.get_month_data(time1, today)
    # apscheduler()
    # xlsx_work()
    # work_it_2()
    # work_it_one_day()

    # p1 = Process(target=java_task, name='java程序')
    # p2 = Process(target=apscheduler, name='定时抓取')
    # p1.start()
    # p2.start()
    work_it_hour()
    # work_it_one_day()