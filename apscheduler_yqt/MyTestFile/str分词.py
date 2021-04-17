# -*- coding: utf-8 -*-
"""
   File Name：     str分词
   Description :
   Author :       hike
   time：          2021/4/16 13:12
"""
import re
str='"{"sn":"19259aa889af41559cf54a4540c66f99","url":"https://weibo.com/ttarticle/p/show?id=2309404626242803728709"}"'
pattern=re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
s=re.findall(pattern,str)
print(s)
s2='{"sn":"19259aa889af41559cf54a4540c66f99","url":"https://weibo.com/ttarticle/p/show?id=2309404626242803728709"}'
print(s2.split('"')[3])
print(eval(s2))