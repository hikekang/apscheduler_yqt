#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/22 16:59
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
def replace_char1(string,char,index):
    string = list(string)
    string[index] = char
    return ''.join(string)

def replace_char2(old_string, char, index):
    '''
    字符串按索引位置替换字符
    '''
    old_string = str(old_string)
    # 新的字符串 = 老字符串[:要替换的索引位置] + 替换成的目标字符 + 老字符串[要替换的索引位置+1:]
    new_string = old_string[:index] + char + old_string[index+1:]
    return new_string
str1="((白岩松)|(郎咸平|郎平)|(罗永浩)|(聂海胜)|(吴京+(于谦|谢楠|狼牙))|(钟南山)|)"
print(replace_char1(str1,"",-2))