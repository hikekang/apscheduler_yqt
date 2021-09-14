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
import gzip
import re
import os
from io import BytesIO

import pika
import time
import datetime
import traceback
from yuqingtong import config
from utils.mylogger import logger
from gne import GeneralNewsExtractor
from utils.sedn_msg import send_feishu_msg
from selenium.webdriver.common.by import By
from utils.webdriverhelper import MyWebDriver
from utils.spider_helper import SpiderHelper
from apscheduler.triggers.cron import CronTrigger
from utils.webdriverhelper import WebDriverHelper
# from utils import qinbaobing_ssql as ssql_helper
from utils import ssql_helper_test as ssql_helper
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        print("使用cookie登录")
        print("cookie_login")
        if cookie_login:
            with open('cookie.json', "r") as f:
                cookie_list = eval(f.read())
            driver.get('http://yuqing.sina.com/yqMonitor')
            for cookie in cookie_list:
                driver.add_cookie(cookie)
            driver.get("http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist")
        else:
            driver.delete_all_cookies()
            time.sleep(1)
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
            time.sleep(1)

        # try:
            # wait = self.wait.until(
            #     EC.invisibility_of_element_located((By.XPATH, "//input[@formcontrolname='userName']")))
            # print(wait)
            # print("登录成功")
        time.sleep(10)
        if driver.current_url=="http://yuqing.sina.com/staticweb/#/yqmonitor/index/yqpage/yqlist":
            logger.info("登录成功")
            cookies=driver.get_cookies()
            if cookie_login==False:
                with open('cookie.json',"w+") as f:
                    f.write(str(cookies))
            return True
        else:
            send_feishu_msg("登录失败，再次尝试登录")
            return  self._login(count=count + 1)
        #     TODO写入数据库
        # except Exception as e:
        #     logger.warning(e)

    # 解析页面进行数据抓取和保存
    def parse_data(self,datacenter_id):
        """
        解析页面生成数据
        :return: 数据已字典形式存在list中
        """
        driver = self.spider_driver
        # i = 2
        post_data=""
        max_page_num = self._maxpage
        config_max_page = int(myconfig.getValueByDict("spider_config", "maxpage"))
        if max_page_num > config_max_page:
            max_page_num = config_max_page
        for request in driver.requests[::-1]:
            if request.response:
                if request.url=="http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList":
                    #  压缩数据进行解压
                    response_data=request.response.body
                    buff=BytesIO(response_data)
                    f_data=gzip.GzipFile(fileobj=buff)
                    # this_all_data=request.response.body.decode().replace("true","True").replace("false","False").replace("null","None")
                    this_all_data=f_data.read().decode().replace("true","True").replace("false","False").replace("null","None")
                    this_all_data=eval(this_all_data)
                    if this_all_data['data']['maxpage']==max_page_num:
                        if this_all_data['data']['page']==self._currentpage:
                            logger.info("匹配到了")
                            post_data=this_all_data
                            break
        if post_data=="":
            logger.info("没有数据")
            return False
        else:
            xpath_data={
                "page_source_data":post_data,
                "info":self.info,
                "datacenter_id":datacenter_id
            }
            queue_name = myconfig.getValueByDict("queue", "name")
            self.channel.basic_publish(exchange='',
                                  routing_key=f'{queue_name}_xpath',
                                  body=str(xpath_data))
            logger.info("发送")
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
                        EC.presence_of_all_elements_located((By.XPATH, '//td')))
                except TimeoutException:
                    error_info="%s-----页面加载出现问题%s"%(self.info['customer'],traceback.format_exc())
                    send_feishu_msg(error_info)
                    ssql_helper.record_error_info(error_info,self.info['customer'])
                    return False
            logger.info("页面加载完全")
            return True
        except TimeoutException as e:
            logger.warning(e)
            logger('再次判断')
            return self._is_page_loaded(count=count + 1)
    def _turn_page(self, max_page_num,time_sleep):
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
            logger.info(f"当前第【{self.next_page_num}】页,共{max_page_num}页")
            self.parse_data(i)
            logger.info('数据抓取完毕')
            # 数据进行处理
            # 上传数据,每页抓取
            if self.next_page_num >= 25:
                logger.info("抓取到最大页，停止")
                return True
            self.next_page_num += 1
            logger.info(f"点击下一页.....")
            if self._currentpage==self._maxpage:
                print("抓取到当前最大页面停止抓取")
                return True
            else:
                try:
                    next_page = self.spider_driver.find_element_by_xpath('//li[contains(@title,"下一页")]')
                    self.spider_driver.execute_script("arguments[0].click();", next_page)
                except Exception as e:
                    error_info="%s------点击下一页出错%s"%(self.info['customer'],traceback.format_exc())
                    logger(error_info)
                    send_feishu_msg(error_info)
                    ssql_helper.record_error_info(error_info,self.info['customer'])
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
        logger.info("%s-----选择时间:%s~~~%s"%(self.info['customer'],start_time,end_time))
        try:
            zidingyi=driver.find_element_by_xpath('//span[contains(text(),"自定义")]')
            time.sleep(0.1)
            zidingyi.click()
            time.sleep(0.1)
            # start_input = driver.find_element_by_xpath('//input[@placeholder="开始时间"]')
            start_i = driver.find_element_by_xpath('//input[@placeholder="开始时间"]/following-sibling::span/i')
            start_i.click()
            time.sleep(0.2)
            start_input = driver.find_element_by_xpath('//div[@class="ant-calendar-date-input-wrap"]/input')
            # ant-calendar-picker-input ant-input ng-star-inserted
            time.sleep(0.2)
            start_input.clear()
            time.sleep(0.2)
            start_input.send_keys(start_time)
            time.sleep(0.2)
            start_deal_button=driver.find_element_by_xpath('//a[@class="ant-calendar-ok-btn "]')
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
            primary=driver.find_element_by_xpath('//button[@nztype="primary"]/span[contains(text(),"确认")]')
            # action = ActionChains(driver)
            # action.move_to_element(primary).perform()
            # time.sleep(0.2)
            # action.click()
            driver.execute_script("arguments[0].click();", primary)
            # primary.click()
            time.sleep(0.2)
            checkbox_list=[]
            checkbox_li=self.spider_driver.find_elements_by_xpath('//div[@class="monitor-info-origin rel ng-star-inserted"]//li')
            for checkbox in checkbox_li:
                tag=checkbox.text.split('\n')[0]
                checkbox_list.append({
                    f"{tag}":checkbox
                })
            for key,value in eval(self.myconfig.getValueByDict("crawl_condition","static_web_condition")).items():
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
                        driver.execute_script("arguments[0].click();",checkbox)
                        time.sleep(0.2)
                else:
                    if checkbox.is_selected():
                        driver.execute_script("arguments[0].click();", checkbox)
                        time.sleep(0.2)
            allinfo=self.spider_driver.find_element_by_xpath("//span[contains(text(),'全部信息')]")
            asc_time=self.spider_driver.find_element_by_xpath("//span[contains(text(),'时间升序')]")
            # allinfo.click()
            driver.execute_script("arguments[0].click();", allinfo)
            time.sleep(0.5)
            # asc_time.click()
            driver.execute_script("arguments[0].click();", asc_time)
            time.sleep(0.5)
            dingxiang_flag=eval(myconfig.getValueByDict("crawl_condition","dingxiang"))
            if dingxiang_flag:
                source_dom = self.spider_driver.find_element_by_xpath('//a[text()=" 定向信源 "]')
                # source_dom.click()
                driver.execute_script("arguments[0].click();", source_dom)
                time.sleep(0.5)

            logger.info("点击查询")
            self.next_page_num = 1
            find_all=driver.find_element_by_xpath("//span[text()='查询']/parent::button")
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", find_all)
            logger.info("查询完毕")
            return True
        except Exception as e:
            error_info="%s-----设置查询条件出错%s"%(self.info['customer'],traceback.format_exc())
            logger.info(error_info)
            send_feishu_msg(error_info)
            ssql_helper.record_error_info(error_info,self.info['customer'])
            return False

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
        if self._set_conditions(self.last_end_time, self.next_end_time):
            return True

        # TODO 时间二分进行查询，尽量避免大于5000条数据的时间
        if not self._is_data_count_outside():  # 没有超过5000条，不用调整
            logger.info(f"小于{config.MAX_DATA_COUNT}条,符合条件")
        else:
            logger.info(f"页面数据大于{config.MAX_DATA_COUNT}条，调整时间区段")
            send_feishu_msg(f"页面数据大于{config.MAX_DATA_COUNT}条，调整时间区段")
            return False


    def _switch_data_count_perpage(self):
        #
        """
        点击每页100条按钮
        :return:
        """
        if not self._is_page_loaded():
            logger.info("更改100条数据/每页前，页面加载有问题")
            return False
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        time.sleep(2)
        self.spider_driver.scroll_to_bottom(10000)
        time.sleep(1)
        try:
            button_js = 'document.querySelector("body > app-root > layout-default > section > ' \
                        'app-index > div > div.yqt-yqmonitor-content.p15 > app-yq-yqlist > div > ' \
                        'div.content > app-monitor-list > nz-card > div > app-info-list >' \
                        ' nz-spin > div > div > nz-table > nz-spin > div > nz-pagination >' \
                        ' ul > div > nz-select > div > div > div").click()'
            self.spider_driver.execute_script(button_js)
            # self.spider_driver.find_element_by_xpath('//div[contains(@title,"50 条/页")]/following-sibling::span').click()
            time.sleep(1)
            self.spider_driver.find_element_by_xpath('//li[contains(text(),"200 条")]').click()
            print('选择100')
            # if not self._is_page_loaded():
            #     logger.info("更改100条数据/每页后，页面加载有问题")
            #     return False
            logger.info("更改200条数据/每页")
            return True
        except Exception as e:
            error_info="%s-------更改页面数量出错%s"%(self.info['customer'],traceback.format_exc())
            logger.info(error_info)
            send_feishu_msg(error_info)
            ssql_helper.record_error_info(error_info,self.info['customer'])
            return False
    def _go_page_num_by_conditions(self,is_reload):
        """
        根据条件和页数进入某一特定页面
        如：2020-01-01 00:00:00 至2020-01-02 00:00:00 第10页
        :return:
        """
        if is_reload:
            self._reload()

        # 设置时间
        if self._adapt_time_interval():
            logger.info("时间和条件设置完毕")
            return True
        else:
            return False

    @property
    def _maxpage(self):
        # 获取最大页数
        try:
            page_max_num = self.spider_driver.find_element_by_xpath('//li[@class="ant-pagination-simple-pager ng-star-inserted"]')
            time.sleep(0.5)
            page_max_num=page_max_num.get_attribute("title")
            # re.findall("\s(\d+)",page_max_num)
            # print(page_max_num[0])
            page_number=int(page_max_num.split("/")[0])
            page_max_num=int(page_max_num.split("/")[1])
            return page_max_num
        except:
            error_info=f"{self.info['customer']}查找最大页数出错"+traceback.format_exc()
            send_feishu_msg(error_info)
            ssql_helper.record_error_info(error_info,self.info['customer'])

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
        total_number=0
        checkbox_list = []
        checkbox_li = self.spider_driver.find_elements_by_xpath(
            '//div[@class="monitor-info-origin rel ng-star-inserted"]//li')
        for checkbox in checkbox_li:
            tag = checkbox.text.split('\n')[0]
            number=checkbox.text.split('\n')[-1]
            checkbox_list.append({
                f"{tag}": checkbox,
                "number":int(number)
            })
        for item in checkbox_list:
            this_number=item['number']
            checkbox = list(item.values())[0].find_element_by_xpath('./label/span/input')
            if checkbox.is_selected():
                total_number+=this_number
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
    def _crawl(self, time_sleep):
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
            if self._is_page_loaded():
                pass
            max_page_num = self._maxpage
            print(f"最大页数：{max_page_num}")

            self.yqt_total_number=self._count_number
            # max_page_num = self._maxpage
            time.sleep(5)
            if self.yqt_total_number!=0:
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
            else:
                return "the number is 0"
    def modifi_keywords_new(self):
        """
        关键词修改
        :return:
        """
        try:
            logger.info("更改关键词")
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
            banzi.click()
            time.sleep(2)
            driver.find_element_by_xpath('//li[@class="ant-dropdown-menu-item ng-star-inserted"]').click()
            time.sleep(1)
            keywords = driver.find_element_by_xpath('//div[@id="senior-area"]')
            time.sleep(0.3)
            keywords.clear()
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
            return True
        except Exception as e:
            logger.info(e)
            error_info="%s------%s设置关键词出错:%s"%(str(datetime.datetime.now()),self.info['customer'],traceback.format_exc())
            logger.info(error_info)
            send_feishu_msg(error_info)
            ssql_helper.record_error_info(error_info,self.info['customer'])
            return False

    def start(self, start_time, end_time, time_sleep, info,channel):
        # 1.登录
        self.interval = [start_time, end_time]
        self.last_end_time = self.interval[0]
        self.next_end_time = self.interval[1]
        # 抓取数据
        self.channel=channel
        logger.info("获取关键词")
        self.info = info
        self.keyword = info['keywords']
        self.SimultaneousWord = info['simultaneouswords']
        self.excludewords = info['excludewords']
        # 重新设置项目路径

        # 设置关键词

        # 添加了关键词判断,并且进行重新设置
        i=0;
        while i<3:
            modifi_keywords_result=self.modifi_keywords_new()
            i+=1
            if modifi_keywords_result==True:
                break


        # 抓取数据并记录
        resp = self._crawl(time_sleep)
        if resp==True:
            logger.info("全部抓取完毕，结束")
        elif resp=="the number is 0":
            logger.info("本次查询数据量为0")

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
    industry_keywords=myconfig.getValueByDict('industry_info','industry_keywords')
    # 获取项目名字
    project_name=eval(myconfig.getValueByDict("industry_info", "project_name"))
    print(project_name)
    for d in customer_list_data:
        print(d['customer'])
        print(d)
        if d['industry_name'] in industry_keywords:
            if d['customer'] in project_name:
                if d['keywords']!='':
                    time_1=time.time()
                    yqt_spider = YQTSpider(myconfig)
                    cookie_login = eval(myconfig.getValueByDict('spider_config', 'cookie_login'))
                    print(cookie_login)
                    # 1.登录
                    if not yqt_spider._login(cookie_login=cookie_login):
                        # raise Exception("登录环节出现问题")
                        ssql_helper.record_error_info("登录失败",d['customer'])
                        send_feishu_msg("%s:登录失败"%d['customer'])
                    else:
                        logger.info("登录成功")
                    credentials = pika.PlainCredentials('qb_01', '123456')
                    connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host='127.0.0.1', port=5672, virtual_host='/', credentials=credentials, heartbeat=0))

                    channel = connection.channel()
                    chromedriver_path = myconfig.getValueByDict('chromerdriver', 'path')

                    chrome_service = Service(chromedriver_path)
                    chrome_service.start()
                    queue_name=myconfig.getValueByDict("queue","name")
                    channel.queue_declare(queue=f'{queue_name}_xpath', durable=True)
                    yqt_spider.start(start_time=start_time, end_time=end_time, time_sleep=2, info=d,channel=channel)
                    logger.info("完成一轮花费时间为：%s"%str(time.time()-time_1))
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
                    work_it(myconfig, start_time, end_time)
            else:
                work_it(myconfig,t_1,t_2)
        else:
            work_it(myconfig,t_1, t_2)


def work_it_one_day(myconfig):
    """
    补抓前一天的数据
    从当前时刻 的前一天数据
    :param myconfig:
    :return:
    """

    now_time = int(time.time())
    day_time_ago = now_time - 86400
    # 一天数据分成3次抓取也就是抓取的间隔时间为4小时
    for i in range(day_time_ago, now_time, 14400):
        start_time_pre = i
        end_time_pre = start_time_pre + 14400
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_pre))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time_pre))
        print(start_time, end_time)
        work_it(myconfig, start_time, end_time)


def apscheduler(myconfig):
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
    sched.add_job(work_it_hour, trigger1, max_instances=10, id='my_job_id', kwargs={'myconfig': myconfig})
    # 每天进行数据补抓一次
    sched.add_job(work_it_one_day, tigger_hour, max_instances=10, id='my_job_id_ever', kwargs={'myconfig': myconfig})
    # 进行数据统计
    # sched.add_job(ssql_helper.find_day_data_count, trigger2, max_instances=10, id='my_job_id_ever_count',
    #               kwargs={'myconfig': myconfig})
    # 生成报表
    sched.add_job(ssql_helper.record_day_datas, trigger3, max_instances=10, id='my_job_id_ever_record_count')
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

    try:

        today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        myconfig = config.redconfig()
        industry_name = myconfig.getValueByDict('industry_info', 'industry_name')

        # ssql_helper.get_month_data(time1, today, industry_name,flushall=False)

        # p1 = Process(target=java_task, name='java程序')
        # p2 = Process(target=apscheduler, kwargs={'myconfig': myconfig}, name='定时抓取')
        # p1.start()
        # p2.start()
        # # print("运行结束")
        work_it_hour(myconfig)
        # apscheduler(myconfig)
    except:
        logger.info(traceback.format_exc())
        send_feishu_msg(traceback.format_exc())



