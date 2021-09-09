#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/17 16:52
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01提取数字.py
 Description:
 Software   : PyCharm
"""
import re
n1=re.findall("\s(\d+).*","/ 100 ")
n1=re.findall("/(\d+).*","2/100")
print(n1)

page_max_num="2/100"
page_number=page_max_num.split("/")[0]
page_max_num=page_max_num.split("/")[1]
print(page_number)
print(page_max_num)