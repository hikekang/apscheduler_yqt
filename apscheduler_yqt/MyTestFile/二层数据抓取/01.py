# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/4/26 13:49
"""
import datetime
import time
import requests
from fake_useragent import  UserAgent
url='http://yuqing.sina.com/newEdition/getDetail.action'
headers={
    'User-Agent':UserAgent().random,
    'Cookie':'LOGIN_KEY=a8999383ceb1b82ad39d50164e35ad24; Hm_lvt_d535b0ca2985df3bb95f745cd80ea59e=1619321791,1619337563,1619416119,1619494308; Hm_lpvt_d535b0ca2985df3bb95f745cd80ea59e=1619494308; Hm_lvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619321791,1619337563,1619416119,1619494308; Hm_lpvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619494308; www=userSId_yqt365_hbslxx_239715_17425; JSESSIONID=4F0678BDBA81455FF183016C9BCC7ACC'
}
params={
    'icc.id':'41619409864496585732171',
    'kw.keywordId':'2685993'
}
start =time.time()
proxies={'http':None,'https':None}
r=requests.post(url=url,headers=headers,params=params,proxies=proxies).text
print(r)
import json
data=json.loads(r)
print(data)
print(data['icc']['content'])
# String or binary data would be truncated
print(time.time()-start)
"""
首先从TS_A库中的各个表中获取未爬取二级数据的连接
    方案一：
        或者更改表结构、重新创建一个表（id,industry_id,ic_id,keyword_id,is_crawl_data）
        查表获取信息，获取行业id，爬取数据，更新 TS_A,QBB_A,TS_B,QBB_B四个库中相对应的行业表
    方案二：
        每隔一段时间扫描表
        各个表增加字段
        查询TS_A库18个行业表，获取 id,industry_id,ic_id,keyword_id
        爬取二级数据 更新库
    方案三：
        mq发送消息队列id,industry_id,ic_id,keyword_id  实时
        爬取数据，更新 TS_A,QBB_A,TS_B,QBB_B四个库中相对应的行业表
        
        
        


"""


end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
start_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
start_time1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
end_time1 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
print(end_time1)
