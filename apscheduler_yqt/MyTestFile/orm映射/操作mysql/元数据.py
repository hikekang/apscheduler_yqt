#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/26 14:11
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 元数据.py
 Description:
 Software   : PyCharm
"""
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String,create_engine
config_info={
    'user':'root',
    'password':'root',
    'host':'localhost',
    'port':3306,
    'dbname':'seo'
}

content_sql="mysql+mysqldb://{user}:{password}@{host}/{dbname}".format(**config_info)

engine=create_engine(content_sql)


metadata = MetaData()
user_table = Table(
"user_account",
     metadata,
     Column('id', Integer, primary_key=True),
     Column('name', String(30)),
     Column('fullname', String(30))
 )
print(user_table.c.name)
print(user_table.c.keys())
# metadata.create_all(engine)


from sqlalchemy import insert

stmt=insert(user_table).values(name="hike",fullname="haidong")
print(stmt)

compiled=stmt.compile()
print(compiled.params)