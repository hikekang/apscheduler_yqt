#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/20 15:06
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : id.py
 Description:
 Software   : PyCharm
"""
import hashlib
salt='http://auto.ifeng.com/yuncheng/jiangjia/2021/0520/511303.shtml'
md = hashlib.md5()  # bytes
md.update(salt.encode('utf-8')) # encode
re = md.hexdigest()
print(re)