#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/21 9:44
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : selenium_web_yqt_apscheduler.py
 Description:
 Software   : PyCharm
"""
#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/15 9:59
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : selenium_web_yqt.py
 Description:使用浏览器模拟人工操作进行数据抓取
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
import json
# 教程
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
    def parse_data(self):
        """
        解析页面生成数据
        :return: 数据已字典形式存在list中
        """
        driver = self.spider_driver
        page_source = driver.page_source
        return self._parse(page_source)
    def _parse(self, page_source):
        p = re.compile("r'\s*|\t|\r|\n'")
        doc = etree.HTML(page_source)
        item_trs = doc.xpath('.//tr[@class="ng-scope"]')
        time.sleep(0.2)
        data_list = []
        for tr in item_trs[1:]:
            tds = tr.xpath('.//td')
            # print(len(tds))
            # 内容
            td_title = tds[1]
            # 来源
            td_orgin = tds[3]
            # 文章站点
            site_name = td_orgin.xpath('span')[0].text

            # 文章时间
            td_time = tds[4].xpath('.//span[@class="date"]/text()')

            def parse_time(td_time):
                from datetime import datetime
                ymd_1 = p.sub("", td_time[0])
                # ymd_2 = td_time.find('span:last-child').text()
                ymd_2 = p.sub("", td_time[1])
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

            # 转发类型  原创 有一部分是没有的 在这里只进行微博的判断
            if site_name=="新浪微博":
                sort_1 = td_title.xpath('.//span[contains(@ng,"icc.repostsFlg!=0")]/text()')
                if len(sort_1) > 0:
                    sort = p.sub("", sort_1[0])
                else:
                    sort = "原创"
            else:
                sort="原创"

            # 获取内容所有文本
            content = p.sub("", td_title.xpath('.//div[contains(@class,"item-title news-item-title contenttext ng-binding")]')[0].xpath(
                'string(.)'))
            # 获取转发内容的所有文本
            spread = td_title.xpath('.//div[contains(@class,"should-spread-area")]')
            spread_content=''
            if spread:
                spread_content = p.sub("", spread[0].xpath('string(.)'))
            else:
                spread_content = ''
            # 针对于文章是标题  针对于微博是作者
            author = td_title.xpath('.//div[contains(@class,"profile-title inline-block")]/a')[0].xpath('string(.)').replace("\n","")
            author_or_title = p.sub("", author)
            if site_name == '新浪微博':
                author = author_or_title
            else:
                result_a_t = author_or_title.split(":")
                result_a_t_1 = author_or_title.split("：")

                if len(result_a_t) >= 2 :
                    author = result_a_t[0]
                    title=result_a_t[1]
                elif len(result_a_t_1)>=2:
                    author = result_a_t_1[0]
                    title = result_a_t_1[1]
                else:
                    author=''
                    if result_a_t_1:
                        title= result_a_t_1[0]
                    if result_a_t:
                        title=result_a_t[0]
            # 行业
            # industry = p.sub("", td_title.xpath('.//div[@class="profile-tip inline-block"]/nz-tag[2]/span/text()')[0])
            # 关键词
            relate_words = p.sub("", td_title.xpath('.//span[@ng-bind="icc.referenceKeyword"]')[0].xpath('string(.)'))
            # 转发数量
            # forwarding_span = td_title.xpath(
            #     './/i[contains(@class,"anticon font-size-16 mr5")]/following-sibling::span')
            # if forwarding_span:
            #     forwarding_num = p.sub("", td_title.xpath(
            #         './/i[contains(@class,"anticon font-size-16 mr5")]/following-sibling::span')[0].text)
            # else:
            #     forwarding_num = 0
            # # 评论数量
            # comment_num_span = td_title.xpath(
            #     './/i[contains(@iconfont,"fa-pinglunshu")]/following-sibling::span/text()')
            # if comment_num_span:
            #     comment_num = comment_num_span[0]
            # else:
            #     comment_num = 0
            # img_src = ",".join([img.attrib['src'] for img in td_title.xpath('//img')])
            # attitude = p.sub("", td_title.xpath('.//div[@class="sensitive-status-content fmg"]')[0].text)
            # ]/div/div[2]/div[1]/div[2]/nz-tag
            # attitude = p.sub("", td_title.xpath('./div[contains(@class,"sensitive-status-content fmg")]/span/text()')[0])
            # //*[@id="news-content_316266263107310667912626"]/div[3]/div[1]/div[1]/div/div[2]
            # //*[@id="news-content_316266263107310667912626"]/div[3]/div[1]/div[1]/div/div[2]
            # attitude = p.sub("", td_title.xpath('./div/div[3]/div[1]/div[1]/div/div[2]/span')[0].xpath("string(.)"))
            attitude = p.sub("", td_title.xpath('.//div[contains(@class,"sensitive-status-content") and not(contains(@class,"ng-hide"))]')[0].xpath(".//span")[0].text)
            title_time = parse_time(td_time)
            print(author,attitude,title_time)

            source_url=td_title.xpath('.//div[@class="btn-group inline-block"]/ul/li[4]/a/@href')[0]
            data = {
                '时间': title_time,
                '标题': title if title!='' else content,
                '描述': content,  # 微博原创
                '链接': source_url,
                '转发内容': spread_content+content+relate_words,
                '发布人': author,
                'attitude': attitude,
                'sort': sort,
                'related_words': relate_words,
                'site_name': site_name,
                'area': p.sub("", td_orgin.xpath('.//div[contains(@ng-if,"icc.province!")]')[0].text),
                'C_Id': self.info['id']  # 客户id
            }
            # if item['forwarderImages']:
            #     for item_pic in item['forwarderImages']:
            #         data['images']+=item_pic['bmiddlePic']
            # if data['sort'] == '原创':
            #     data['转发内容'] = spread+content+relate_words
            # if len(data['标题']) > 20:
            #     data['标题'] = data['标题'][0:20]
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
            positive_dict = {
                "敏感": 0.1,
                "非敏感": 0.9,
                "中性": 0.65
            }
            data['positive_prob_number'] = positive_dict[attitude.split()[0]]
            data_list.append(data)
        return data_list

    # 数据处理
    def clear_data(self, data_list):
        logger.info("数据处理")
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
            #2.转发微博并且转发内容为空的使舍去
            elif data["标题"] == "转发微博" and data["转发内容"] == "":
                # new_data_list.remove(data)
                print("标题为转发微博，转发内容为空")
                continue
            #3.转发类型的微博，取前内容的前20个字符作为标题
            elif data["标题"] == "转发微博":
                if len(data["转发内容"]) >= 50:
                    data["标题"] = data["转发内容"][0:20]
                    data['描述'] = data["转发内容"][0:120]
                else:
                    data["标题"] = data["转发内容"]
                    data['描述'] = data["转发内容"]

            if data['描述'] != "" and data["转发内容"] == "" and len(data["转发内容"]) == 0:
                data["转发内容"] = data['描述']

            if data['转发内容'] != "" and data['描述'] == "" and len(data['转发内容']) != 0:
                # if len(data["转发内容"]) >= 20:
                #     data["标题"] = data["转发内容"][0:20]
                # else:
                #     data['描述'] = data['转发内容']
                data['描述'] = data['转发内容']

            if data['描述']=="转发微博" and data["转发内容"] != "":
                if len(data["转发内容"]) >= 50:
                    data['描述'] = data['转发内容'][0:120]
                else:
                    data['描述']=data['转发内容']

            if "微博" in data['site_name']:
                # print("处理标题")
                data['标题'] =data['描述'][0:20]
            if len(data['描述']) > 120:
                # print("处理描述")
                data['描述'] = data['描述'][0:120]

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
            sec_list.append(data)
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
            data_list = self.parse_data()
            logger.info('数据抓取完毕')
            # 数据进行处理
            data_list = self.clear_data(data_list)

            # 插入到数据库，返回一个成功插入的值
            # 上传数据,每页抓取
            if data_list:
                ssql_helper.upload_many_data(data_list, self.industry_name, i, self.info)
                # ssql_helper.upload_many_data_java(data_list, self.industry_name, i)
                logger.info(f"解析到{len(data_list)}条数据")
                self.post_number += len(data_list)
                logger.info(f"保存完毕")
                # SpiderHelper.save_xlsx(data_list=data_list, out_file=self.data_file_path, sheet_name=self.industry_name)
                logger.info(f"保存完毕")
                time.sleep(time_sleep)
            # 想要抓取的最大页数，可以修改
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
        start_time = start_time.strftime(config.DATETIME_FORMAT)
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

        if not eval(self.myconfig.getValueByDict("crawl_condition","all")):
            time.sleep(0.2)
            self.spider_driver.find_element_by_xpath("//input[@id='wb']").click()
            time.sleep(0.5)
            self.spider_driver.find_element_by_xpath("//input[@id='wx']").click()
            time.sleep(0.5)
            self.spider_driver.find_element_by_xpath("//input[@id='sp']").click()
            time.sleep(0.5)
            self.spider_driver.find_element_by_xpath("//input[@id='lt']").click()
        time.sleep(0.5)
        print("点击查询")
        driver.find_element_by_xpath("//a[@id='searchListButton']").click()
        return True
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
        # logger.info(
        #     f"当前时间区间:{self.last_end_time.strftime(config.DATETIME_FORMAT)}  --"
        #     f" {self.next_end_time.strftime(config.DATETIME_FORMAT)}")


    def _switch_data_count_perpage(self):
        #
        """
        点击每页100条按钮
        :return:
        """
        self.spider_driver.get("http://yuqing.sina.com/yqmonitor")
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

        if self.next_page_num > 1:
            logger.info(f"直接进入第{self.next_page_num}页")
            self.spider_driver.find_element_by_xpath(
                '//input[@class="ant-input ng-untouched ng-pristine ng-valid"]').send_keys(
                self.next_page_num)
            time.sleep(0.5)
            self.spider_driver.find_element_by_xpath('//span[contains(text(),"确定")]').click()
        if not self._is_page_loaded():
            logger.info("直接进入第多少页时页面加载出现问题")
            return False
        page_num = int(self.spider_driver.find_element_by_xpath('//span[@ng-bind="page"]').text)
        if int(page_num) != self.next_page_num:
            logger.warning("页面上当前页面和应该进入的页面不一样，请检查")
            return False
        logger.info("进入成功")
        return True

    @property
    def _maxpage(self):
        # 获取最大页数
        page_max_num = int(self.spider_driver.find_element_by_xpath('//span[@ng-bind="maxpage"]').text)
        print(page_max_num)
        return page_max_num

    @property
    def _count_number(self):
        return int(self.spider_driver.find_element_by_xpath('//span[@ng-bind="originStat.total"]').text)
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

            ret = self.keyword.split("|")
            keywords = []
            for i in range(0, len(ret), 3):
                key = ''
                for j in ret[i:i + 3]:
                    key += j + '|'
                keywords.append(key)
            # 多关键词抓取
            self.yqt_total_number=self._count_number
            # if self._count_number > 5000:
            #     for keyword in keywords:
            #         input_keywords = self.spider_driver.find_element_by_xpath(
            #             '//input[@class="ant-input ng-untouched ng-pristine ng-valid ng-star-inserted"]')
            #         input_keywords.clear()
            #         input_keywords.send_keys(keyword)
            #         time.sleep(1)
            #         self.spider_driver.find_element_by_xpath(
            #             '//i[@class="anticon anticon-search ng-star-inserted"]').click()
            #         if self._is_page_loaded():
            #             max_page_num = self._maxpage
            #             # 翻页并抓取数据
            #             resp = self._turn_page(max_page_num, time_sleep)
            #             if resp == "restart_browser":
            #                 return resp
            #             elif not resp:
            #                 self._turn_page(max_page_num, time_sleep)
            #                 if turn_page_reload_count >= 3:
            #                     logger.warning("翻页时，连续出现问题3次，退出")
            #                     return False
            #                 turn_page_reload_count += 1
            #                 is_reload = True
            #                 continue
            #             turn_page_reload_count = 0
            #             # 翻页结束
            #
            #             # 设置下次抓取条件
            #             self.next_page_num = 1
            #             if self.next_end_time >= self.interval[1]:
            #                 logger.info("解析到终止时间，抓取完成")
            #                 logger.info("全部抓取完毕上传数据")
            #                 logger.info("开始记录")
            #                 # 舆情通数量
            #                 yqt_count = self._count_number
            #                 record_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            #                                                 f"record\{self.project_name}", f"{self}_记录.xlsx")
            #                 sql_number = ssql_helper.find_info_count(self.interval[0], self.interval[1],
            #                                                          self.industry_name)
            #                 data_list = [self.project_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            #                              self.last_end_time, self.next_end_time]
            #                 SpiderHelper.save_record_auto(record_file_path, yqt_count, self.post_number, sql_number,
            #                                               data_list=data_list)
            #                 # record_dict = (self.industry_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.last_end_time,
            #                 # self.next_end_time, yqt_count, self.post_number, self.project_name)
            #
            #                 record_dict = (
            #                     self.industry_name,  # 行业名称
            #                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 抓取时间
            #                     self.last_end_time,  # 开始时间
            #                     self.next_end_time,  # 结束时间
            #                     yqt_count,  # 舆情通数量
            #                     self.post_number,  # 上传数量
            #                     self.project_name,  # 项目名称
            #                     self.first_len,  # 第一次过滤之后的数量
            #                     self.redis_len  # redis过滤之后的数量
            #                 )
            #
            #                 # 数据统计记录
            #                 ssql_helper.record_log(record_dict)
            #                 # SpiderHelper.save_record(record_file_path,yqt_count,xlsx_num,post_info['number'],post_info2['number'],sql_number,data_list=data_list)
            #                 return True
            #             else:
            #                 self.last_end_time = self.next_end_time  # 上次终止时间就是下次起始时间
            #                 self.next_end_time = self.interval[1]

            # else:
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
        driver = self.spider_driver
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

    def start(self, start_time, end_time, time_sleep, info, is_one_day):
        # try:
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
        self.spider_driver.refresh()
        if not self._is_page_loaded():
            return False
        return True


# 自定义时间抓取任务
def work_it(myconfig, start_time, end_time):
    # 获取驱动文件路径
    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')
    chrome_service = Service(chromedriver_path)
    chrome_service.start()
    yqt_spider = YQTSpider(myconfig, start_time=start_time, end_time=end_time)

    customer_list_data = ssql_helper.get_industry_keywords()


    # 根据项目进行抓取，方便统计
    # 获取行业名字
    industry_keywords=myconfig.getValueByDict('industry_info','industry_keywords')
    # 获取项目名字
    project_name=myconfig.getValueByDict('industry_info','project_name')
    print(project_name)
    for d in customer_list_data:
        print(d)
        if d['industry_name'] in industry_keywords:
            if d['customer'] in project_name:
                if d['keywords']!='':
                    yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=d, is_one_day=False)
                    print("完成一轮")

    if yqt_spider.spider_driver.service.is_connectable():
        print("进入finally2")
        yqt_spider.spider_driver.close()
        print("关闭")
    chrome_service.stop()


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
    #按天进行抓取
    elif list(time_info.keys())[0] == 'days':
        days = int(time_info['days'])
        end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d ") + "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        work_it(myconfig, start_time, end_time)
    # 自定义的时间
    elif list(time_info.keys())[0] == 'myself_days':
        myself_days=eval(myconfig.getValueByDict('time_info','myself_days'))
        t_1=myself_days[0]
        t_2=myself_days[1]
        interval_hour=myself_days[-1]*3600
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
                    work_it(myconfig, start_time, end_time)
            else:
                work_it(t_1,t_2)
        else:
            work_it(t_1, t_2)


def work_it_one_day(myconfig):
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
        work_it(myconfig, start_time, end_time)


def apscheduler(myconfig):
    # 日常cron
    cron_info = myconfig.getDictBySection('cron_info')
    print(cron_info["daily_cron"])
    trigger1 = CronTrigger.from_crontab(cron_info["daily_cron"])
    tigger_hour = CronTrigger.from_crontab(cron_info['hour_cron'])
    # 每天记录
    trigger2 = CronTrigger.from_crontab(cron_info['day_record_cron'])

    sched = BlockingScheduler()
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id', kwargs={'myconfig': myconfig})
    # 每天进行数据补抓一次
    sched.add_job(work_it_one_day, tigger_hour, max_instances=10, id='my_job_id_ever', kwargs={'myconfig': myconfig})
    # 进行数据从统计
    sched.add_job(ssql_helper.find_day_data_count, trigger2, max_instances=10, id='my_job_id_ever_count',
                  kwargs={'myconfig': myconfig})
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
    time1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    myconfig = config.redconfig()
    industry_name = myconfig.getValueByDict('industry_info', 'industry_name')
    # ssql_helper.get_month_data(time1, today, industry_name,flushall=False)

    # p1 = Process(target=java_task, name='java程序')
    p2 = Process(target=apscheduler, kwargs={'myconfig': myconfig}, name='定时抓取')
    # p1.start()
    p2.start()
    # # print("运行结束")
    work_it_hour(myconfig)

    # print("抓取结束")
    # # except Exception as e:
    # #     my_e = my_Email()
    # #     my_e.send_message(str(e), "程序预警")
    # # # work_it_hour()