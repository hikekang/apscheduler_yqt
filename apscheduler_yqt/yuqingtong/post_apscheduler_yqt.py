#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/18 16:09
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : post_apscheduler_yqt.py
 Description:
 Software   : PyCharm
"""

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
from utils import ssql_helper_test as ssql_helper
import re
from selenium.webdriver.chrome.service import Service
from multiprocessing import Process
# from utils.email_helper import my_Email
from lxml import etree
from utils.post_helper import SecondData
from concurrent.futures import ThreadPoolExecutor

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
    def _parse(self, payload):
        positive_dict = {
            "惊奇": 0.1,
            "喜悦": 0.9,
            "中性": 0.5
        }
        data_list = []
        # 带有二层数据的数据
        secod_content = SecondData(self.cookie, payload).get_content()
        if secod_content!=None:
            for item in secod_content['data']['icontentCommonNetList']:
                data = {
                    # '时间': item['captureTime'].replace("T"," ").replace(".000+0000",""),
                    '时间': item['publishedMinute'],
                    '标题': ex(item['title']) if item['title']!=None else item['title'],
                    '描述': ex(item['content']) if item['content']!=None else item['content'],  # 微博原创
                    '链接': item['webpageUrl'],
                    '转发内容': ex(item['forwarderContent']) if item['forwarderContent']!=None else item['forwarderContent'],
                    '发布人': item.get('author'),
                    'ic_id': item['id'],
                    'keywords_id': item['keywordId'],
                    # attitude:item['distrution']
                    'attitude': item['emotion'],
                    'images':"" ,
                    'reposts_count': item['forwardNumber'],
                    'comments_count': 0,
                    'sort': '转发' if int(item['repostsFlg'])==1 else '原创',
                    'industry': ",".join(item['secondTradeList']),
                    'related_words': item['referenceKeyword'],
                    'site_name': item['captureWebsiteName'],
                    # 'area': item['contentAddress'],
                    'area': item['province'],
                    'C_Id':self.info['id']# 客户id
                }
                if item['forwarderImages']:
                    for item_pic in item['forwarderImages']:
                        data['images']+=item_pic['bmiddlePic']
                if data['sort'] == '原创':
                    data['转发内容'] = data['描述']
                if len(data['标题']) > 20:
                    data['标题'] = data['标题'][0:20]

                if data['发布人']:
                    if '：' in data['发布人'] or ":" in data['发布人']:
                        publish_man = re.sub(':|：', '', data['发布人'])
                        # publish_man=data['发布人'].split(":")[0]
                        data['发布人'] = publish_man
                    else:
                        if (len(data['发布人']) > 10):
                            data['发布人'] = ''
                    if (len(data['发布人']) > 15):
                        data['发布人'] = ''
                if data['attitude']=='中性':
                    data['positive_prob_number'] = 0.5
                elif data['attitude']=='喜悦':
                    data['positive_prob_number'] = 0.1
                else:
                    data['positive_prob_number']=0.9
                data_list.append(data)
            return data_list
        else:
            return None
    # more placeholders in sql than params available

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
                    data['描述'] = data["转发内容"][0:20]
                else:
                    data["标题"] = data["转发内容"]
                    data['描述'] = data["转发内容"]

            if data['描述'] != "" and data["转发内容"] == "" and len(data["转发内容"]) == 0:
                data["转发内容"] = data['描述']

            if data['转发内容'] != "" and data['描述'] == "" and len(data['转发内容']) != 0:
                if len(data["转发内容"]) >= 20:
                    data["标题"] = data["转发内容"][0:20]
                else:
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
        # logger.info("数据处理花费时间:", t2 - t1)
        # logger.info("数据处理完毕之后的数量", len(sec_list))
        return sec_list

    # 第一次根据爬取链接去重
    def quchong(self, dir_list, key):
        logger.info("第一次链接去重之前数据量为：%s",str(len(dir_list)))
        new_dirlist = []
        values = []
        for d in dir_list:
            if d[key] not in values:
                new_dirlist.append(d)
                values.append(d[key])

        self.first_len += len(new_dirlist)
        logger.info("第一次滤重之后的数量:%s", str(self.first_len))

        # 本次打开浏览器直至抓取结束的数据量

        return new_dirlist

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
                    (By.XPATH, '//span[@class="ant-spin-dot ant-spin-dot-spin ng-star-inserted"]')))
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

    def _reload(self):
        """
        刷新页面
        :return:
        """
        self.spider_driver.refresh()
        if not self._is_page_loaded():
            return False
        return True

    def _save_process(self):
        with open(self.process_file_path, "w", encoding="utf-8") as f:
            f.write(f"{self.interval[0]}至{self.interval[1]}|"
                    f"{self.last_end_time}_{self.next_end_time}_{self.next_page_num}_{self.data_file_path}")

    def _turn_page(self, time_sleep):
        # 资源上锁
        lock = threading.Lock()
        def thread_all(i):
            payload_all = {"searchCondition": {
                "keywordId": int(self.keyword_id),
                "accurateSwitch": 1,
                "bloggerAuthenticationStatusMultiple": "0",
                "blogPostsStatus": 0,
                "comblineflg": 2,
                "dataView": 0,
                "displayIcon": 1,
                "involveWay": 0,
                "keywordProvince": "全部",
                "matchType": 3,
                "ocrContentType": 0,
                "searchRootWbMultiple": "0",
                "timeDomain": "-1",
                "weiboTypeMultiple": "0",
                "secondKeywordMatchType": 1,
                "searchSecondKeyword": "",
                "webSiteId": "0",
                "order": 2,
                "monitorType": 1,
                "isRoot": 1,
                "origins": "1",
                "presentResult": "1",
                "options": "1",
                "attributeCheck": "1",
                "informationContentType": 1,
                "duplicateShowMultiple": "0",
                "startTime": str(self.last_end_time),
                "endTime": str(self.next_end_time),
                "attribute": "1",
                "chartStart": str(self.last_end_time),
                "chartEnd": str(self.next_end_time),
                "page": 1,
                "pageSize": 100
            }}

            payload_all['searchCondition']['page'] = i
            # 数据进行处理
            raw_data=self._parse(payload_all)
            data_list = self.clear_data(raw_data)
            logger.info('数据抓取完毕')
            # 插入到数据库，返回一个成功插入的值
            # 上传数据
            if data_list:
                # 数据上传
                ssql_helper.upload_many_data(data_list, self.industry_name,i,self.info)
                logger.info(f"正在抓取第{i}页数据")
                logger.info(f"解析到{len(data_list)}条数据")
                self.post_number += len(data_list)
                lock.acquire()
                SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path, sheet_name=self.industry_name)
                lock.release()
                logger.info(f"保存完毕")
                time.sleep(time_sleep)
        def thread_part(keyword,datacenter_id):
            logger.info(f"本次抓取的关键词为：{keyword}")
            payload_part = {"searchCondition": {"keywordId": int(self.keyword_id), "accurateSwitch": 1,
                                                "bloggerAuthenticationStatusMultiple": "0",
                                                "blogPostsStatus": 0, "comblineflg": 2, "dataView": 0, "displayIcon": 1,
                                                "involveWay": 0,
                                                "keywordProvince": "全部", "matchType": 3, "ocrContentType": 0,
                                                "searchRootWbMultiple": "0",
                                                "searchType": '', "timeDomain": "1", "weiboTypeMultiple": "0",
                                                "firstOrigin": '',
                                                "sencondOrigin": '', "secondKeywordMatchType": 1,
                                                "searchSecondKeyword": '',
                                                "webSiteId": "0", "order": 2, "monitorType": 1, "isRoot": 1,
                                                "origins": "1",
                                                "presentResult": "1", "options": "1", "attributeCheck": "1",
                                                "informationContentType": 1,
                                                "duplicateShowMultiple": "0", "attribute": "1",
                                                "chartStart": str(self.last_end_time),
                                                "chartEnd": str(self.next_end_time), "page": 1, "pageSize": 100}}
            # payload_part['searchCondition']['searchSecondKeyword'] = "({0})+({1})".format(keyword, self.SimultaneousWord)
            payload_part['searchCondition']['searchSecondKeyword'] = keyword
            # print(payload_part)
            content_all = SecondData(self.cookie, payload_part).get_content_by_keywords()
            if content_all != None:
                maxpage = int(content_all['data']['maxpage'])
                print("最大页数为%d",maxpage)
                if maxpage != 0:
                    if maxpage>50:
                        # maxpage=50
                        maxpage = int(self.myconfig.getValueByDict('spider_config', 'maxpage'))
                    for i in range(1, maxpage + 1):
                        payload_part['searchCondition']['page'] = i
                        logger.info(f"抓取的关键字为{payload_part['searchCondition']['searchSecondKeyword']}，抓取到第{i}页")
                        content = self._parse(payload_part)
                        if content != None:
                            data_list = self.clear_data(content)
                            if data_list:
                                # datacenter_id  词的id
                                ssql_helper.upload_many_data(data_list,self.industry_name,datacenter_id,self.info)
                                logger.info(f"解析到{len(data_list)}条数据")
                                self.post_number += len(data_list)
                                # SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path,sheet_name=self.info['sheet_name'])
                                # lock.acquire()
                                # SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path,
                                #                        sheet_name=self.industry_name)
                                # lock.release()
                                logger.info(f"保存完毕")
        """
        翻页
        :return:
        """
        # 首先查询全部
        payload_all = {"searchCondition": {
            "keywordId": int(self.keyword_id),
            "accurateSwitch": 1,
            "bloggerAuthenticationStatusMultiple": "0",
            "blogPostsStatus": 0,
            "comblineflg": 2,
            "dataView": 0,
            "displayIcon": 1,
            "involveWay": 0,
            "keywordProvince": "全部",
            "matchType": 3,
            "ocrContentType": 0,
            "searchRootWbMultiple": "0",
            "timeDomain": "-1",
            "weiboTypeMultiple": "0",
            "secondKeywordMatchType": 1,
            "searchSecondKeyword": "",
            "webSiteId": "0",
            "order": 2,
            "monitorType": 1,
            "isRoot": 1,
            "origins": "1",
            "presentResult": "1",
            "options": "1",
            "attributeCheck": "1",
            "informationContentType": 1,
            "duplicateShowMultiple": "0",
            "startTime": str(self.last_end_time),
            "endTime": str(self.next_end_time),
            "attribute": "1",
            "chartStart": str(self.last_end_time),
            "chartEnd": str(self.next_end_time),
            "page": 1,
            "pageSize": 100
        }}
        content_all = SecondData(self.cookie, payload_all).get_content()
        self.post_number = 0
        # 返回内容不为空
        if content_all!=None:
            total_count=content_all['data']['totalCount']
            self.yqt_total_number = total_count
            maxpage=content_all['data']['maxpage']
            logger.info(f'数据总量为{total_count}')
            logger.info(f'总页数为{maxpage}')
            if total_count>5000:
                logger.info("数据量太大需要分词抓取")
                ret = self.keyword.split("|")
                keywords = []
                for i in range(0, len(ret), 3):
                    key = ''
                    for j in ret[i:i + 3]:
                        key += j + '|'
                    keywords.append(key)
                # 分词查询
                crawlerThreads = []
                # for datacenter_id,keyword in enumerate(keywords):
                #     thread=threading.Thread(target=thread_part,kwargs={'keyword':keyword,"datacenter_id":datacenter_id+1})
                #     crawlerThreads.append(thread)
                # for thread in crawlerThreads:
                #     thread.start()
                # for thread in crawlerThreads:
                #     thread.join()



                # pool = ThreadPool()
                # pool.map(thread_part, keywords)
                # pool.close()
                # pool.join()

                # update on 2021-05-25 11:20:57
                with ThreadPoolExecutor(1) as pool:
                    for datacenter_id,item in enumerate(self.info['project_words']):
                        pool.submit(thread_part,item['keywords'],datacenter_id+1)
                    logger.info("分词抓取完毕")
                return True

            elif(total_count<5000 and maxpage>0 ):
                # crawlerThreads=[]
                # for i in range(1,maxpage+1):
                #     thread=threading.Thread(target=thread_all,kwargs={'i':i})
                #     crawlerThreads.append(thread)
                # for thread in crawlerThreads:
                #     thread.start()
                # for thread in crawlerThreads:
                #     thread.join()

                #update on 2021-05-25 11:22:06
                with ThreadPoolExecutor(1) as pool:
                    for i in range(1,maxpage+1):
                        pool.submit(thread_all, i)

                    # pool = ThreadPool()
                # pool.map(thread_part, range(0,maxpage+1))
                # pool.close()
                # pool.join()
                return True
        else:
            return False

    def _crawl2(self, time_sleep):
        """

        :param time_sleep:
        :return:
        """
        # 翻页并抓取数据
        resp = self._turn_page(time_sleep)
        if resp:
            # 设置下次抓取条件
            if self.next_end_time >= self.interval[1]:
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
                SpiderHelper.save_record_auto(record_file_path, yqt_count, self.post_number, sql_number_A,sql_number_B,
                                              data_list=data_list)
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
                    self.project_name,  # 项目名称
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
        else:
            return False
    def modifi_keywords_new(self):
        #     yqt_tree_li act ng-star-inserted
        driver = self.spider_driver
        logger.info("点击")
        span = driver.find_element_by_xpath('//span[@class="yqt_tree_li act ng-star-inserted"]')
        span.click()
        driver.switch_to.window(driver.window_handles[1])
        # 获取keywords_id
        keyword_id = driver.current_url.split("=")[-1]
        self.keyword_id = keyword_id
        doc = etree.HTML(driver.page_source)
        # self.userSearchSetId=doc.xpath('//input[@id="view.userSearchSetId"]')[0].text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        banzi = span.find_element_by_xpath('.//i[@class="anticon ant-dropdown-trigger"]')
        action = ActionChains(driver)
        time.sleep(1)
        # 移动到该元素
        action.move_to_element(span).perform()
        time.sleep(3)
        banzi.click()
        time.sleep(2)
        driver.find_element_by_xpath('//li[@class="ant-dropdown-menu-item ng-star-inserted"]').click()
        time.sleep(1)
        keywords = driver.find_element_by_xpath('//div[@id="senior-area"]')
        keywords.clear()
        keywords.clear()
        time.sleep(0.3)
        # if self.SimultaneousWord:
        #     keyword = "({0})+({1})".format(self.keyword, self.SimultaneousWord)
        # else:
        #     keyword = self.keyword
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

        web_cookies = self.spider_driver.get_cookies()
        ck = ''
        for cookie in web_cookies:
            ck = ck + cookie['name'] + "=" + cookie['value'] + ";"

        # 设置完关键词之后获取cookie
        self.cookie = ck

    def start(self, start_time, end_time, time_sleep, info, is_one_day):
        try:
            # 1.登录
            if not self._login():
                raise Exception("登录环节出现问题")
            self.interval = [start_time, end_time]
            self.last_end_time = self.interval[0]
            self.next_end_time = self.interval[1]
            # 抓取数据
            logger.info("获取关键词")
            self.info = info
            self.keyword = info['keywords']
            self.SimultaneousWord = info['simultaneouswords']
            self.excludewords = info['excludewords']
            self.C_Id=info['id']
            # 重新设置项目路径

            self.data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                               f"data\{self.project_name}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
                                               f"{self}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{start_time}_{end_time}.xlsx".replace(
                                                   ':', '_'))
            logger.info(self.data_file_path)
            # 设置关键词
            self.modifi_keywords_new()

            # 抓取数据并记录
            resp = self._crawl2(time_sleep)
            if resp:
                logger.info("全部抓取完毕，结束")
                    # pyautogui.alert("抓取完成...")
        except Exception as e:
            logger.warning(e)
        # finally:
        #     print("进入finally")
        #     if self.spider_driver.service.is_connectable():
        #         print("进入finally2")
        #         self.spider_driver.quit()
        #         self.spider_driver.close()
        #         print("关闭")


# 自定义时间抓取任务
def work_it(myconfig, start_time, end_time):
    # 获取项目信息
    # from xlsx
    # infos = config.row_list
    # from config.ini
    # myconfig = config.redconfig()
    # 获取驱动文件路径
    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')
    chrome_service = Service(chromedriver_path)
    chrome_service.start()

    # yqt_spider = YQTSpider(infos[0], start_time=start_time, end_time=end_time)
    yqt_spider = YQTSpider(myconfig, start_time=start_time, end_time=end_time)

    p_data = []
    customer_list_data = ssql_helper.get_industry_keywords()

    # project_list = ssql_helper.merger_industry_data(customer_list_data)
    # for project_data in project_list:
    #     if project_data['industry_name'] == yqt_spider.industry_name:
    #         p_data.append(project_data)
    # logger.info(p_data)

    # 根据项目进行抓取，方便统计
    industry_keywords=myconfig.getValueByDict('industry_info','industry_keywords')
    for d in customer_list_data:
        if d['industry_name'] in industry_keywords:
            if d['keywords']!='':
                yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=d, is_one_day=False)
                print("完成一轮")

    if yqt_spider.spider_driver.service.is_connectable():
        print("进入finally2")
        yqt_spider.spider_driver.close()
        print("关闭")
    chrome_service.stop()


def work_it_hour(myconfig):
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
    elif list(time_info.keys())[0] == 'days':
        days = int(time_info['days'])
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig, start_time, end_time)


def work_it_one_day(myconfig):
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


def apscheduler(myconfig):
    trigger1 = CronTrigger(hour='0-23', minute='01', second=00, jitter=5)
    cron_info = myconfig.getDictBySection('cron_info')
    # for key,value in cron_info.items():
    #     cron_info[key]=eval(value)
    tigger_hour = CronTrigger(**cron_info)
    trigger2 = CronTrigger(hour='0', minute='01', second=00, jitter=5)
    sched = BlockingScheduler()
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id',kwargs={'myconfig':myconfig})
    # sched.add_job(work_it_one_day, trigger2, max_instances=10, id='my_job_id_ever',kwargs={'myconfig':myconfig})
    sched.add_job(work_it_one_day, tigger_hour, max_instances=10, id='my_job_id_ever',kwargs={'myconfig':myconfig})
    sched.add_job(ssql_helper.find_day_data_count, trigger2, max_instances=10, id='my_job_id_ever_count',kwargs={'myconfig':myconfig})
    sched.start()


def java_task():
    ab = os.path.dirname(os.path.realpath(__file__))
    path_java = os.path.join(ab, "jms-1.1.1.jar")
    # print(path_java)
    print('java程序')
    command = r'java -jar ' + path_java
    os.system(command)
    print("执行成功")


if __name__ == '__main__':
    # try:
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time1 = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    myconfig = config.redconfig()
    print("加载数据")
    industry_name=myconfig.getValueByDict('industry_info', 'industry_name')
    ssql_helper.get_month_data(time1, today,industry_name)
    # print("加载完毕")
    # xlsx_work()
    # work_it_2()
    # work_it_one_day()
    # print('开始运行')

    p1 = Process(target=java_task, name='java程序')
    # # p2 = Process(target=apscheduler,kwargs={'myconfig':myconfig},name='定时抓取')
    p1.start()
    # # p2.start()
    # # print("运行结束")
    work_it_hour(myconfig)
    # # except Exception as e:
    # #     my_e = my_Email()
    # #     my_e.send_message(str(e), "程序预警")
    # # # work_it_hour()