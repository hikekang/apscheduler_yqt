# -*- coding: utf-8 -*-
"""
   File Name：     路径测试
   Description :
   Author :       hike
   time：          2021/5/6 16:52
"""
import os

# current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录
current_work_dir = os.getcwd()  # 当前文件所在的目录
print(os.getcwd())
weight_path = os.path.join(current_work_dir, 'jms-1.1.1.jar')  # 再加上它的相对路径，这样可以动态生成绝对路径
# print(current_work_dir)
print(weight_path)

config_path=os.path.join(os.path.dirname(os.getcwd()),'config.xlsx')
print(config_path)