#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/26 14:07
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 使用orm会话执行.py
 Description:
 Software   : PyCharm
"""
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import text
config_info={
    'user':'root',
    'password':'root',
    'host':'localhost',
    'port':3306,
    'dbname':'seo'
}

content_sql="mysql+mysqldb://{user}:{password}@{host}/{dbname}".format(**config_info)

engine=create_engine(content_sql)
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)

with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with Session(engine) as session:
    result = session.execute(text("UPDATE some_table SET y=:y WHERE x=:x"),[{"x": 1, "y":11}, {"x":2, "y": 15}])