# -*- coding: utf-8 -*-
"""
   File Name：     seqserver_helper
   Description :
   Author :       hike
   time：          2021/4/1 14:44
"""
import re
from utils.snowflake import IdWorker
import pymssql
from utils import post_mq
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
connect_A=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_A',port='39999',charset='utf8')
connect_B=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='TS_B2.0',port='39999',charset='utf8')
connect_QBBA=pymssql.connect(server='223.223.180.9',user='tsuser1',password='tsuser1@123aA',database='QBB_A',port='39999',charset='utf8')
cursor_A=connect_A.cursor()
cursor_B=connect_B.cursor()
cursor_QBBA=connect_QBBA.cursor()

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
def insert_data_list(data_list):

    pass

# B库中查询项目名称以及行业名称
def get_industry_name():

    sql_B="select * from TS_Customers where IsEnable=1"
    cursor_B.execute(sql_B)
    # get enable project
    data=cursor_B.fetchall()

    new_data=[]
    for d in iter(data):
        # 处理乱码
        new_d={
            'id':'',
            'customer':'',
            'industry_name':'',
            'keywords':'',
            'excludewords':'',
            'simultaneouswords':'',
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
def post_data(data_list,industry_name):
    table_name = tables[industry_name]
    sql_industry_id="select id from TS_Industry where name='"+industry_name+"'"
    print(sql_industry_id)
    # sql_industry_id="select id from TS_Industry wh"

    cursor_B.execute(sql_industry_id)

    industry_id =cursor_B.fetchone()[0]
    for data in data_list:
        worker = IdWorker(1, 2, 0)
        id=worker.get_id()
        sql_ts_a ="insert into {}(id,industry_id,title,summary,content,url,author,publish_time) values (id,industry_id,data['标题'],data['描述'],data['转发内容'],data['链接'],data['发布人'],data['时间']) ".format(table_name)
        sql_qbb_a ="insert into {}(id,industry_id,title,summary,content,url,author,publish_time,is_original,loaction) values (id,industry_id,data['标题'],data['描述'],data['转发内容'],data['链接'],data['发布人'],data['时间'],data['is_original'],data['area']) ".format(table_name)
        cursor_A.execute(sql_ts_a)
        data={
            'id':id,
            'industry_id':industry_id
        }
        post_mq('reptile.stay.process',data)
        cursor_QBBA.execute(sql_qbb_a)
        post_mq('reptile.stay.process_2.1',data)
