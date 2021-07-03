#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/2 10:28
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import os
# 获取当前文件路径
print(os.path.abspath(__file__))

print(__file__)
# 获取当前文件所在文件夹路径
print(os.path.abspath(os.path.dirname(__file__)))

print(os.path.join(os.path.dirname(os.path.abspath(__file__)),f"record\hike",f"roday.xlsx"))
print(os.path.join(os.path.dirname(os.path.abspath(__file__)),f"record\hike",f"roday.xlsx"))

record_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                f"record\{'hike'}", f"_记录.xlsx")
print(record_file_path)