#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/22 10:42
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : re1.py
 Description:
 Software   : PyCharm
"""
import requests
for i in range(100):
    url = 'http://localhost:8090/jms/send?queues=%s&message={"id":%s,"industryId":%s}' % (
                'reptile.stay.process_2.2221', str(i), 'industry_id')
    # requests.get('http://localhost:8090/jms/send',params=params)
    # print(url)
    proxies = {'http': None, 'https': None}
    # proxies = {"http": None, "https": None}
    requests.get(url, proxies=proxies)