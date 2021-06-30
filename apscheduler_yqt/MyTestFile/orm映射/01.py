#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/25 17:37
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""

# 导入:
from sqlalchemy import Column, String, create_engine,Integer,BIGINT,VARCHAR,DateTime,REAL,Text
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from models import *
# 创建对象的基类:

def InsertDataList(session,data_list):
    session.add_all(data_list)
if __name__ == '__main__':

    # 初始化数据库连接:
    # engine = create_engine('mssql+pymssql://sa:P@ssw0rd@192.168.1.240/sandisk?charset=utf8')
    conn_info={
        'username':'hike',
        'password':123456,
        'host':'123',
        'database':123
    }
    conn_sql='mssql+pymssql://{username}:{password}@{host}/{database}/?charset=utf8'.format(**conn_info)
    print(conn_sql)
    # engine = create_engine('mssql+pymssql://sa:33221100@192.168.0.77/TS_A/?charset=utf8',pool_size=20,max_overflow=0)
    # # 创建DBSession类型:
    # DBSession = sessionmaker(bind=engine)
    #
    # session=DBSession()
    #
    # session.add_all(TSIndustryNewsCirculation_base())
    # session.query()
    # session.commit()