# -*- coding: utf-8 -*-
"""
   File Name：     os_filepath
   Description :
   Author :       hike
   time：          2021/3/31 16:27
"""
import os
import datetime

print(os.path.exists(r'F:\项目\sina_yuqing\51_yqt\test\os_filepath.py'))
print(r'F:\项目\sina_yuqing\51_yqt\test\os_filepath.py')
data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data",
                                           f"{'hike'}_{11}_{11}_{22}_{33}.xlsx".replace(':','_'))
print(type(data_file_path))
print(repr(data_file_path).split("'")[1])
path=repr(data_file_path).split("'")[1]
# print(os.path.exists(path))
# print(os.path.exists(data_file_path))


dir = os.path.dirname(data_file_path)
print(type(dir))

print(os.path.exists(data_file_path))