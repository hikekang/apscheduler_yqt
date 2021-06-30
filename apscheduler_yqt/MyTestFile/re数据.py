# -*- coding: utf-8 -*-
"""
   File Name：     re数据
   Description :
   Author :       hike
   time：          2021/4/18 9:45
"""
import requests

params = {
    'queues': 'dss',
    'message': 'data'
}
r=requests.get('http://localhost:8090/jms/send', params=params)
print(r.text)
