# -*- coding: utf-8 -*-
"""
   File Name：     seqserver_helper
   Description :
   Author :       hike
   time：          2021/4/1 14:44
"""
from datetime import datetime
from utils.snowflake import IdWorker
import pymssql
from utils import getdatabyselenium
from utils import post_mq
from utils import baidu_emition
import redis
import time
import re
pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
r=redis.Redis(connection_pool=pool)
config={
    'server':'223.223.180.9',
    'user':'tuser1',
    'password':'tsuser1@123aA',
    'database':'TS_A',
    'port':'39999'
}
connect=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',port='39999')
cursor=connect.cursor()
connect_A=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',
                          port='39999',charset='utf8',autocommit=True)
connect_B=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_B2.0',
                          port='39999',charset='utf8',autocommit=True)
connect_QBBA=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='QBB_A',
                             port='39999',charset='utf8',autocommit=True)
connect_QBBB=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='QBB_B',
                             port='39999',charset='utf8',autocommit=True)
cursor_A=connect_A.cursor()
cursor_B=connect_B.cursor()
cursor_QBBA=connect_QBBA.cursor()
cursor_QBBB=connect_QBBB.cursor()

'''
优速 流通贸易
一嗨  汽车业
'''
tables = {
        "餐饮业": "dbo.TS_industry_news_catering",
        "保险业": "dbo.TS_industry_news_insurance",
        "房地产": "dbo.TS_industry_news_estate",
        "服务业": "dbo.TS_industry_news_service",
        "公关传统": "dbo.TS_industry_news_PR",
        "IT业": "dbo.TS_industry_news_IT",
        "教育": "dbo.TS_industry_news_education",
        "金融业": "dbo.TS_industry_news_financial",
        "机械制造": "dbo.TS_industry_news_machine",
        "流通贸易": "dbo.TS_industry_news_circulation",
        "旅游业": "dbo.TS_industry_news_tourism",
        "汽车业": "dbo.TS_industry_news_automotive",
        "食品业": "dbo.TS_industry_news_food",
        "文化出版": "dbo.TS_industry_news_cultural",
        "医疗保健": "dbo.TS_industry_news_medical",
        "其它": "dbo.TS_industry_news_other",
    }

def find_info_count(start_time,end_time,industry_name):
    connect=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',port='39999')
    cursor=connect.cursor()
    table_name=tables[industry_name]
    sql="select count(*) from {table_name} where publish_time between '{start_time}' and '{end_time}' ".format(table_name=table_name,start_time=start_time,end_time=end_time)

    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time>='2021-04-02 10:00:00' and create_time<='2021-04-02 11:00:00'"
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-04-02 10:00:00' and '2021-04-02 11:00:00' "
    print(sql)
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-03-22' and '2021-04-01' "
    cursor.execute(sql)
    # print(type(cursor.fetchall()))
    count=cursor.fetchall()[0][0]
    print(count)
    return count

# B库中查询项目名称以及行业名称 对应的关键词
def get_industry_keywords():
    sql_B="select * from TS_Customers where IsEnable=1"
    cursor_B.execute(sql_B)
    # get enable project
    data=cursor_B.fetchall()
    new_data=[]
    for d in iter(data):
        # 处理乱码
        new_d={
            'id':'',#行业id
            'customer':'',#项目
            'industry_name':'',#行业名称
            'keywords':'',#关键词
            'excludewords':'',#排除词
            'simultaneouswords':'',#同现词
        }
        for i,dd in enumerate(d):
            if i==0:
                new_d['id']=dd
                # 单字段去重
                # sql_A="select distinct Word from TS_Keywords where C_ID={}".format(dd).encode('GBK')
                # sql_A="select Word,Simultaneouswords,Excludewords from TS_Keywords where C_ID={} group by Word".format(dd)
                sql_A="select Word,SimultaneousWord,Excludeword from TS_A.dbo.TS_Keywords where C_ID={} group by Word,SimultaneousWord,Excludeword".format(dd)
                # sql_A="select Word,SimultaneousWord,Excludeword from TS_A.dbo.TS_Keywords where C_ID='1149212304344420353' group by Word,SimultaneousWord,Excludeword"
                cursor_A.execute(sql_A)
                data_A=cursor_A.fetchall()
                for da in data_A:
                    for i,d_a in enumerate(da):
                        if d_a and i==0:
                            new_d['keywords']+=re.sub('、','|',d_a.encode('latin1').decode('gbk'))+'|'
                        if d_a and i==1:
                            new_d['excludewords']+=re.sub('、','|',d_a.encode('latin1').decode('gbk'))+'|'
                        if d_a and i==2:
                            new_d['simultaneouswords']+=re.sub('、','|',d_a.encode('latin1').decode('gbk'))+'|'
            if i==1:
                new_d['customer']=(d[1].encode('latin1').decode('gbk'))
            else:
                new_d['industry_name']=(d[2].encode('latin1').decode('gbk'))
        new_data.append(new_d)
    return new_data

# 上传数据
def post_data(data_list,industry_name):
    table_name = tables[industry_name]
    sql_industry_id="select id from TS_Industry where name='"+industry_name+"'"
    # print(sql_industry_id)
    # sql_industry_id="select id from TS_Industry wh"

    cursor_B.execute(sql_industry_id)

    industry_id =cursor_B.fetchone()[0]
    print(len(data_list))
    for data in data_list:
        worker = IdWorker(1, 2, 0)
        # 生成雪花id
        id=worker.get_id()
        positive_prob=baidu_emition.emotion(data['转发内容'][0:1000])
        time.sleep(0.1)
        sql_ts_a ="insert into %s (id,industry_id,title,summary,content,url,author,publish_time,emotion_status) values (%d,%d,'%s','%s','%s','%s','%s','%s',%f)"%(table_name,id,industry_id,data['标题'],data['描述'],data['转发内容'],data['链接'],data['发布人'],data['时间'],positive_prob)
        sql_qbb_a ="insert into %s (id,industry_id,title,summary,content,url,author,publish_time,is_original,location,emotion_status) values " \
                   "(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%f)"%(table_name,id,industry_id,data['标题'],data['描述'],data['转发内容'],data['链接'],data['发布人'],data['时间'],data['is_original'],data['area'],positive_prob)
        # 插入A库
        cursor_A.execute(sql_ts_a)
        data={
            "id":id,
            "industryId":industry_id
        }
        # 更新redis
        r.sadd(industry_id,data['链接'])

        # 滤重
        # post_mq.send_to_queue('reptile.stay.process',str(data))
        # print("执行")
        # 插入QBB_A库
        cursor_QBBA.execute(sql_qbb_a)
        # 拉取信息到B库
        post_mq.send_to_queue('reptile.stay.process_2.1',str(data))
    print("数据上传成功")

def testsql():
    sql_ts_a = "insert into '%s' (id,industry_id,title,summary,content,url,author,publish_time) values (''%s'','%s','%s','%s','%s','%s','%s','%s')" %('hike','hike','hike','hike','hike','hike','hike','hike','hike',)
    print(sql_ts_a)
    # 插入A库

# 将所有行业的数据加载到内存中
def get_month_data(time1,time2):
    r.flushall()
    for tb in tables.values():
        sql="select industry_id,url from %s where publish_time between '%s' and '%s'"%(tb,time1,time2)
        print(sql)
        cursor_A.execute(sql)
        datas=cursor_A.fetchall()
        for d in datas:
            r.sadd(d[0], d[1])

# 根据url进行二次滤重
def filter_by_url(datalist,industry_name):
    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    cursor_B.execute(sql_industry_id)
    industry_id = cursor_B.fetchone()[0]
    new_data_list=[]
    for data in datalist:
        if r.sismember(industry_id,data['链接'])==False:
            new_data_list.append(data)
    return new_data_list
def get_teack_datas():
    sql_of_extend="select SN from TS_DataMerge_Extend where is_Track=1"
    cursor_QBBB.execute(sql_of_extend)
    datas=cursor_QBBB.fetchall()
    url_list=[]
    for data in datas:
        sql_of_base = "select URL from TS_DataMerge_Base where SN='%s'" % (data[0])
        cursor_QBBB.execute(sql_of_base)
        urls=cursor_QBBB.fetchone()
        if "weibo.com" in urls[0]:
            url={
                'sn':data[0],
                'url':urls[0]
            }
            url_list.append(url)
    return url_list
def track_data_number_sql():
    for url in get_teack_datas():
        data=getdatabyselenium.get_data_it(url['url'])
        # data=getdatabyselenium.get_data_it(url['url'])
        create_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     转发、评论、点赞
    sql_record="insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')"%(url['sn'],data[0],data[1],data[2],create_date)
    print(cursor_QBBB.execute(sql_record))
    sql_Base="update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' "%(data[0],data[1],data[2],url['sn'])
    print(cursor_QBBB.execute(sql_Base))

track_data_number_sql()
# import time
# t1=time.time()
# get_month_data('2021-03-14','2021-04-13 10:00:00')
# t2=time.time()
# print(t2-t1)

# print(get_industry_keywords())
