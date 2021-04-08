# -*- coding: utf-8 -*-
"""
   File Name：     正则去掉符号
   Description :
   Author :       hike
   time：          2021/4/8 10:42
"""
import re
s='hike:11：'
print(re.sub(':|：','',s))