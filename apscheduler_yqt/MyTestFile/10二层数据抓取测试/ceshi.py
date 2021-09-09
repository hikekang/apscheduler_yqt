#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/9 14:48
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : ceshi.py
 Description:
 Software   : PyCharm
"""
from utils.ssql_pool_helper import config_test_net,config_QBBB,DataBase
from utils.secodnd_data_utils import crawl_second_by_requests,crawl_second_by_webdriver
import re
from concurrent.futures.thread import ThreadPoolExecutor
web_url_selenium=re.compile('http[s]://(www.toutiao.com)|(mp.weixin.qq.com)|'
                            '(dy.163.com/v2/article/detail)|(kuaibao.qq.com)|(www.sohu.com)|(www.360kuai.com)|(view.inews.qq.com).*')
# web_url_selenium_list=['www.toutiao.com','mp.weixin.qq.com']
video_url=re.compile('http[s]://(v.qq.com)|(live.kuaishou.com)|(www.iesdouyin.com)|(www.ixigua.com)|(m.toutiaoimg.cn).*')
qbb_sql_select="select URL from TS_DataMerge_Base with(NOLOCK) where 'PublishDate_Std'>'2021-08-06 14:00:00' and url not like '%weibo%'"
db_qbbb = DataBase('sqlserver', config_QBBB)
test_db = DataBase('sqlserver', config_test_net)

url_list=db_qbbb.execute_query(qbb_sql_select)

def tt():
    for item in url_list:
        match_selenim = web_url_selenium.findall(item[0])
        if match_selenim:
            content = crawl_second_by_webdriver(item[0])
            if content == "":
                datas = "selenium抓取错误"
            else:
                datas = content
                datas += "通过selenium抓取"
        else:
            match_video = video_url.findall(item[0])
            if match_video:
                datas = "视频正则"
            else:
                content = crawl_second_by_requests(item[0])
                if content == "":
                    datas = "requests抓取错误"
                else:
                    datas = content
        test_insert_sql = "insert into test1 (content,url) values(%s,%s)"
        # print(test_insert_sql,datas,item[0])
        test_db.execute(test_insert_sql, (datas, item[0]))
with ThreadPoolExecutor(4) as pool:
    pool.submit(tt)

