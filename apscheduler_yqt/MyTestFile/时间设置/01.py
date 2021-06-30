# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/4/29 10:07
"""
import datetime
end_time = datetime.datetime.now().strftime('%Y-%m-%d ')+"00:00:00"
start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ")+"00:00:00"
start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
print(start_time,end_time)

str='2021-05-19T02:40:21.000 0000'.replace("T"," ").replace(".000 0000","")
print(str)
t1=datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
print(t1)
st=''
print (22) if st!=None else print(11)