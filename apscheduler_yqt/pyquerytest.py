#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 9:49
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : pyquerytest.py
# @Software: PyCharm

from pyquery import PyQuery as pq
html="<html><span _ngcontent-mqg-c23="">09:12<br>今天</span></html>"
doc=pq(html)
time1=doc.find('span').text()
print(time1)
t1=time1.split('\n')
print(t1)
