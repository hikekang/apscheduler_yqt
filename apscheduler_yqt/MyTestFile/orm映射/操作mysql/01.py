#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/26 13:46
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from sqlalchemy import create_engine
from sqlalchemy import text
# mysql+mysqldb://{user}:{password}@{host}[:{port}]/{dbname}

config_info={
    'user':'root',
    'password':'root',
    'host':'localhost',
    'port':3306,
    'dbname':'seo'
}

content_sql="mysql+mysqldb://{user}:{password}@{host}/{dbname}".format(**config_info)
print(content_sql)
engine=create_engine(content_sql)

with engine.connect() as conn:
    result=conn.execute(text("select 'hello world'"))
    print(result.all())


with engine.connect() as conn:
    # conn.execute(text("create table some_table (x int,y int)"))
    # conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),[{"x": 1, "y": 1}, {"x": 2, "y": 4}])
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")


stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)

with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}  y: {row.y}")












