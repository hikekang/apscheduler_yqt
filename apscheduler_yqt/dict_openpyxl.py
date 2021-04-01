# -*- coding: utf-8 -*-
"""
   File Name：     dict_openpyxl
   Description :
   Author :       hike
   time：          2021/3/31 10:06
"""
from openpyxl import Workbook
def inputexcel(inputdata,outputdata):
    wb = Workbook()
    sheet = wb.active
    fd = inputdata[0]
    for zm,i in list(zip([chr(letter).upper() for letter in range(65, 91)],range(len(list(fd.keys()))))):
        sheet[zm+str(1)].value = list(fd.keys())[i]
    j = 2
    for item in inputdata:
        for zm, key in list(zip([chr(letter).upper() for letter in range(65, 91)], list(fd.keys()))):
            sheet[zm+str(j)] = item[key]
        j += 1
    wb.save(outputdata)
datalist=[]
for i in range(5):
    data={
        'a':i,
        'b':i
    }
    datalist.append(data)
for i,item in enumerate(datalist):
    print(i)
    print(item)
inputexcel(datalist,'12.xlsx')