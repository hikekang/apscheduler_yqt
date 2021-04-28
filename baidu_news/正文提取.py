# -*- coding: utf-8 -*-
"""
   File Name：     正文提取
   Description :
   Author :       hike
   time：          2021/4/28 10:22
"""
from gne import GeneralNewsExtractor
html='<html><body>大容量充电宝*2w毫安【59】拍最后一项79选项，他家充电宝反馈真的超级棒 ，而且用个3年没有问题哈！！2万毫安的电量可以手机三次啦！俩个充电口，可同时充2个设备，出门旅行这个真的很有必要啦！！ ​ ​​'
extractor=GeneralNewsExtractor()
r=extractor.extract(html)
print(r['content'])