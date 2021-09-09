# -*- coding: utf-8 -*-
"""
   File Name：     shijain
   Description :
   Author :       hike
   time：          2021/3/30 15:48
"""
import datetime
# 格式化时间
print(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')  )
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print(datetime.datetime.now().strftime('%Y-%m-%d %H')+":00:00" )
# 往前算一小时
one_hour_ago=datetime.datetime.now()-datetime.timedelta(hours=1)
print(one_hour_ago)
end_time=one_hour_ago.strftime('%Y-%m-%d %H')+":00:00"
print(end_time)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 根据指定的格式把一个时间字符串解析为时间元组。
end_time1=datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
print(type(end_time1))
print(type(end_time))
print(end_time1)

str_end='2021-04-08 00:02:00'
str_end=datetime.datetime.strptime(str_end,'%Y-%m-%d %H:%M:%S')-datetime.timedelta(hours=1)
print(str_end)

