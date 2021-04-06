# -*- coding: utf-8 -*-
"""
   File Name：     seqserver_helper
   Description :
   Author :       hike
   time：          2021/4/1 14:44
"""
import datetime

import pymssql
config={
    'server':'223.223.180.9',
    'user':'tuser1',
    'password':'tsuser1@123aA',
    'database':'TS_A',
    'port':'39999'
}
connect=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',port='39999')
# connect=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',port='39999')
# connect=pymssql.connect(**config)
# print(connect)
cursor=connect.cursor()
# print(cursor)

#
# tables = []
# sql = 'select TABLE_NAME, table_type, engine from information_schema.tables where table_schema="TS_A"'
# try:
#     # 执行查询语句
#     cursor.execute(sql)
#     # 取得所有结果
#     results = cursor.fetchall()
#     # 打印数据表个数
#     print(len(results))
#     # 打印数据表名，数据表类型，及存储引擎类型
#     print("table_name", "table_type", "engine")
#     for row in results:
#         name = row[0]
#         type = row[1]
#         engine = row[2]
#         tables.append(name)
#         print(name, type, engine)
# except Exception as e:
#     raise e
# finally:
#     connect.close()



# sql = 'show tables from TS_A'
# rows = cursor.execute(sql)  # 返回执行成功的结果条数
# print(f'一共有 {rows} 张表')
# for d in cursor.fetchall():
#     for k,v in d.items():
#         print(v)

'''
优速 流通贸易
一嗨  汽车业



'''


def find_info_count(start_time,end_time,industry_name):
# def find_info_count():
    tables={
        "餐饮业":"dbo.TS_industry_news_catering",
        "保险业":"dbo.TS_industry_news_insurance",
        "房地产":"dbo.TS_industry_news_estate",
        "服务业":"dbo.TS_industry_news_service",
        "公关传统":"dbo.TS_industry_news_PR",
        "IT业":"dbo.TS_industry_news_IT",
        "教育":"dbo.TS_industry_news_education",
        "金融业":"dbo.TS_industry_news_financial",
        "机械制造":"dbo.TS_industry_news_machine",
        "流通贸易":"dbo.TS_industry_news_circulation",
        "旅游业":"dbo.TS_industry_news_tourism",
        "汽车业":"dbo.TS_industry_news_automotive",
        "食品业":"dbo.TS_industry_news_food",
        "文化出版":"dbo.TS_industry_news_cultural",
        "医疗保健":"dbo.TS_industry_news_medical",
        "其它":"dbo.TS_industry_news_other",
    }
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
# print(find_info_count())
#
# count=find_info_count('2021-04-02 10:00:00','2021-04-02 11:00:00','流通贸易')
# print(count)
