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
s_2="https://www.toutiao.com/i1703797708472328/"
s_2="https://www.ixigua.com/6978754027341218345"
s_3="https://www.iesdouyin.com "

pattern=re.compile('([(www.toutiao.com)]|[(www.ixigua.com)])')
pattern=re.compile('http[s]://[(m.toutiaoimg.cn),(www.toutiao.com),(www.ixigua.com)].*')
match=pattern.findall(s_3)
print(match)

web_url_selenium=re.compile('http[s]://^(www.toutiao.com)|(mp.weixin.qq.com)|(dy.163.com/v2/article/detail)|(kuaibao.qq.com)|(www.sohu.com).*')
web_url_selenium.findall()