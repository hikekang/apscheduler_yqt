#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 10:41
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""

# 判断一个字符串含有多个字符串中的任意一个
p = "Tom is a boy,Lucy is a girl,they all like english!"
keywords= 'Tom,Lucy'
excludes = ['english','math']
print (any([w in p and w for w in keywords.split(',')]))
print (any(e in p for e in excludes))

# 判断一个字符串含有多个字符串
p = "Tom is a boy,Lucy is a girl,they all like english!"
keywords= 'Tom,Lucy'
filters= ["boy","like"]
print(all(f in p for f in filters))
print(all([w in p and w for w in keywords.split(',')]))

#计算一个字符串含有指定字符串的数量
p = "Tom is a boy,Lucy is a girl,Tom like math and Lucy like english!"
p2 = "id"
keywords= 'english,math,history,laws'
print(sum([1 if w in p and w else 0 for w in keywords.split(',')]))


def contain_keywords(keywords, *str):
    return any(k in ss for ss in str for k in keywords.split("|"))
keywords= 'Tom|Lucy'
print(contain_keywords(keywords,(p,p2)))


