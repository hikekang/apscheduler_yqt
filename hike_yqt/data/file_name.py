# -*- coding: utf-8 -*-
"""
   File Name：     file_name
   Description :
   Author :       hike
   time：          2021/3/31 11:10
"""
#!/usr/bin/python
# -*- coding:utf8 -*-
import os
def getFilePathList(path, filetype):
    pathList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filetype):
                pathList.append(os.path.join(root, file))
    return pathList  # 输出以filetype为后缀的列表

print(os.path.relpath(__file__))
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(".")))

print(os.path.abspath(__file__))

print(os.getcwd())

print(getFilePathList(os.getcwd(),'csv'))

import datetime
today=datetime.datetime.now().strftime('%Y-%m-%d')
print(datetime.datetime.now().strftime('%Y-%m-%d'))
test_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"datas\优速\{today}")
print(test_file)

os.mkdir(test_file)
print("创建成功")