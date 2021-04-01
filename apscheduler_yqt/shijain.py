# -*- coding: utf-8 -*-
"""
   File Name：     shijain
   Description :
   Author :       hike
   time：          2021/3/30 15:48
"""
import datetime
print(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')  )
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print(datetime.datetime.now().strftime('%Y-%m-%d %H')+":00:00" )
one_hour_ago=datetime.datetime.now()-datetime.timedelta(hours=1)
print(one_hour_ago)
end_time=one_hour_ago.strftime('%Y-%m-%d %H')+":00:00"
print(end_time)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
end_time1=datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
print(type(end_time1))
print(type(end_time))
print(end_time1)