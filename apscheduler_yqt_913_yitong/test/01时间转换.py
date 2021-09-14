# _*_coding:utf-8 _*_
# @Time　　:2021/9/13   14:23
# @Author　 : Antipa
# @ File　　  :01时间转换.py
# @Software  :PyCharm
# @Description

from datetime import datetime
str1='2021-09-13 14:23:48'
year=datetime.strptime(str1,"%Y-%m-%d %H:%M:%S").year
print(type(year))
print(datetime.strptime(str1,"%Y-%m-%d %H:%M:%S").month)

print(str(year)+str())