#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 10:51
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : keywords变成列表.py
 Description:
 Software   : PyCharm
"""
# keywords='安能物流|壹米|优速|杨兴运'
keywords=''
list_keywords=list()
ret =keywords.split("|")
print(ret)

str='我要投诉@安能物流电脑显示器破损 没人解决 都在逃避问题 分享自@黑猫投诉 http://t.cn/A6V9PzXl'

print(any(k in str for k in ret))

def test_keywords(key,str):
    for s in str:
        print(s)

# test_keywords('hike',['zhangsan',])
test_keywords('hike',('zhangsan','lisi'))