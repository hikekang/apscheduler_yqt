# -*- coding: utf-8 -*-
"""
   File Name：     excutemany_test
   Description :
   Author :       hike
   time：          2021/4/23 11:11
"""
import pymssql
import random
import time

import requests

config={
    'server':'192.168.0.77',
    'user':'tuser1',
    'password':'tsuser1@123aA',
    'database':'TS_A',
    'port':'39999'
}
connect=pymssql.connect(server='192.168.0.77',user='sa',password='33221100@aA',database='QBB_A',port='1433',autocommit=True)
data_list=[]
cursor=connect.cursor()
t12=time.time()
sql="insert into sql_test (inudstry,id) values (%s,%s)"
for i in range(10):
    inudstry=random.randint(0,100000)
    id=random.randint(0,100000)

    # cursor.execute(sql, (inudstry,id))
    # url='http://localhost:8090/jms/send?queues=%s&message={"id":%s,"industryId":%s}'%('accccc',id,inudstry)
    data={
        'id':id,
        'industryid':inudstry
    }
    # print(url)
    # proxies={'http':None,'https':None}
    # data_list.append(data)
    # proxies = {"http": None, "https": None}
    # requests.get(url,proxies=proxies)
    data_list.append((inudstry,id))

table_name='sql_test'
print(table_name)
sql="insert into "+ table_name+" (inudstry,id) values (%d,%d)"
print(sql)

cursor.executemany(sql,data_list)
print(data_list)
t2=time.time()
print(t2-t12)
# insert into dbo.TS_industry_news_automotive (id,industry_id,title,summary,content,url,author,publish_time,emotion_status) values (%d,%d,'%s','%s','%s','%s','%s','%s',%f)

str=b'\xe9\x93\xb6\xe5\xb7\x9d\xe5\xb8\x82\xe8\xa5\xbf\xe5\xa4\x8f\xe5\x8c\xba110\xe5\x9b\xbd\xe9\x81\x93\xe4\xb8\x8e307\xe5\x9b\xbd\xe9\x81\x93\xe4\xba\xa4\xe5\x8f\x89\xe5\x8f\xa3\xe5\xbe\x80\xe6\xa6\x86\xe6\xa0\x91\xe6\xb2\x9f\xe6\x96\xb9\xe5\x90\x91500\xe7\xb1\xb3\xe5\x8f\x91\xe7\x94\x9f\xe4\xba\xa4\xe9\x80\x9a\xe4\xba\x8b\xe6\x95\x85'
print(str.decode('utf-8'))

# more placeholders in sql than params available


