# -*- coding: utf-8 -*-
"""
   File Name：     路径测试
   Description :
   Author :       hike
   time：          2021/5/8 14:23
"""
import os
import sys
dir_path = os.path.dirname(os.getcwd())
dir_path=os.path.join(dir_path,'log')
log_path = os.path.join(dir_path, 'test.log')
if not os.path.exists(dir_path.encode('utf-8').decode('utf-8')):
    os.mkdir(dir_path.encode('utf-8').decode('utf-8'))
    print("创建成功")

print(os.path.exists(dir_path))
# if not os.path.exists(log_path):
#     with open(log_path,"wb") as f:
#         f.close()

# os.mkdir("张三")
print(os.path.exists('张三'))