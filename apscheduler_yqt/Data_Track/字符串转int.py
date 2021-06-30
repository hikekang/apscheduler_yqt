# -*- coding: utf-8 -*-
"""
   File Name：     字符串转int
   Description :
   Author :       hike
   time：          2021/4/16 9:48
"""

# 既然不能用int函数，那我们就反其道而行，用str函数找出每一位字符表示的数字大写。
def atoi1(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        t = '%s * 1' % v
        n = eval(t)
        num += n * (10 ** i)
    return num

# 利用ord求出每一位字符的ASCII码再减去字符0的ASCII码求出每位表示的数字大写。
def atoi2(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        offset = ord(v) - ord('0')
        num += offset * (10 ** i)
    return num

# eval的功能是将字符串str当成有效的表达式来求值并返回计算结果。我们利用这特点可以利用每位字符构造成和1相乘的表达式，再用eval算出该表达式的返回值就表示数字大写。
def atoi3(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num

print(atoi2('0'))