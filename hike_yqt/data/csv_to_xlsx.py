# -*- coding: utf-8 -*-
"""
   File Name：     csv_to_xlsx
   Description :
   Author :       hike
   time：          2021/3/31 11:19
"""
import pandas as pd
import os
def csv_to_xlsx_pd(filename):
    csv = pd.read_csv(filename, encoding='GBK')
    print(csv)
    for i in csv.keys():
        print(i)
    out_file_name=filename.split('.')[0]+'xlsx'
    csv.to_excel(out_file_name,sheet_name=None)

def getFilePathList(path, filetype):
    pathList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filetype):
                pathList.append(os.path.join(root, file))
    return pathList  # 输出以filetype为后缀的列表

if __name__ == '__main__':
    # file_names=getFilePathList(os.getcwd(),'csv')
    # for f in file_names:
    #     csv_to_xlsx_pd(f)
        # f1=f.split('.')[0]
        # print(f1)
        # print(type(f))

    file_path="F:\项目\sina_yuqing\51_yqt\data\csv_to_xlsx.py"
    print(os.path.exists("F:\项目\sina_yuqing\51_yqt\data\舆情通_zdyousu_2021-03-30 12_00_58_2021-03-18 19_00_00_2021-03-18 23_59_59.csv"))