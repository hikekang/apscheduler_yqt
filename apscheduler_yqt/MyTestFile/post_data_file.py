# -*- coding: utf-8 -*-
"""
   File Name：     post_data_file
   Description :
   Author :       hike
   time：          2021/4/1 21:38
"""
import os
import requests
def getFilePathList(path, filetype):
    pathList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filetype):
                pathList.append(os.path.join(root, file))
    return pathList  # 输出以filetype为后缀的列表
file_list=getFilePathList('F:\项目\sina_yuqing\data\卫浴','xlsx')
post_url="http://localhost:8086/localproject/industry/industryBigDataExcelByEasyExcel"
for i,f in enumerate(file_list):
    print(i+1)
    files={'file':open(f,'rb')}
    proxies = {"http": None, "https": None}
    post_info=requests.post(post_url,files=files,proxies=proxies).text
    post_info = eval(post_info)
    print("导入数据量为{}",post_info['number'])
