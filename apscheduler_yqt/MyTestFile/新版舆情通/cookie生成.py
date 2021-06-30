#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/18 14:26
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : cookie生成.py
# @Software: PyCharm

cookies=[{'domain': 'yuqing.sina.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': False, 'value': '7309C43EE82A37B413794875F752FFD0'}, {'domain': 'yuqing.sina.com', 'expiry': 1621923788, 'httpOnly': True, 'name': 'www', 'path': '/', 'secure': False, 'value': 'userSId_yqt365_lsitit_850894_60500'}]

ck=''
for cookie in cookies:
    ck=ck+cookie['name']+"="+cookie['value']+";"

print(ck)


