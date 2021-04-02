# -*- coding: utf-8 -*-
"""
   File Name：     test_mkdir_xlsx
   Description :
   Author :       hike
   time：          2021/4/2 9:33
"""
import os
import datetime

from openpyxl import Workbook

'''
# 只能创建一级目录
os.mkdir()
#创建多级目录
os.makedirs()


'''

import config
data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"data\{config.info['project_name']}\{datetime.datetime.now().strftime('%Y-%m-%d')}",
                                           f"_{config.info['yuqingtong_username']}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{11}_{22}.xlsx".replace(':','_'))
dir=os.path.dirname(data_file_path)
print(dir)
if not os.path.exists(dir):
    os.makedirs(dir)

if not os.path.exists(data_file_path):
    wb = Workbook(data_file_path)
    wb.save(data_file_path)