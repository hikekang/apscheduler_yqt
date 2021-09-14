#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:43
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : crawl_second_data.py
# @Software: PyCharm


"""
二层数据抓取



"""
from fake_useragent import UserAgent
import requests
import time
import json
from utils import extract_content
import threading

class crawl_second():
    def __init__(self,cookie):
        self.url='http://yuqing.sina.com/newEdition/getDetail.action'
        self.headers= {
        'User-Agent': UserAgent().random,
        'Cookie': cookie
    }

    def crawl_data(self,data,db_qbbb,db_a):
        params = {
            'icc.id': data[2],
            'kw.keywordId': data[3]
        }
        r = requests.post(self.url, params=params, headers=self.headers, proxies={'http': None, 'https': None})
        time.sleep(0.3)
        print(r.text)
        data_content = json.loads(r.text)
        # print(data_content)
        # 获取数据
        content = extract_content.extract_content(str('<html><body>' + data_content['icc']['content']))
        # print(content+"\n")
        # B库更新
        sql_Base = "update TS_DataMerge_Base set Body='%s'where url='%s' " % (content, data[5])
        print(sql_Base)
        db_qbbb.execute(sql_Base)

        sql_second_data = "update TS_Second_Data set crawl_flag=1 where url='%s'" % data[5]
        db_a.execute(sql_second_data)

    def second_data_url_sql(self,db_a):
        """
        二层数据抓取 url查询
        """
        sql="select * from TS_Second_Data where crawl_flag=0"
        data=db_a.execute_query(sql)
        return data


    def multi_thread(sefl):
        """
        多线程数据爬取
        """
        threads=[]
        for data in iter(sefl.second_data_url_sql()):
            threads.append(
                threading.Thread(target=sefl.crawl_data,args=(list(data),))
            )
        for thread in threads:
            thread.start()
    
        for thread in threads:
            thread.join()
    
    def single_thread(sefl):
        for data in iter(sefl.second_data_url_sql()):
            sefl.crawl_data(data)