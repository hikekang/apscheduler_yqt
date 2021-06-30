#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/2 16:41
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import uuid
uid=uuid.uuid1()
print(str(uid).split('-'))
print(''.join(str(uid).split('-')))
print(uuid.uuid3(uuid.NAMESPACE_DNS, 'yuanlin'))
print(uuid.uuid4())
print(uuid.uuid5(uuid.NAMESPACE_DNS, 'yuanlin'))
