# -*- coding: utf-8 -*-
"""
   File Name：     连接池
   Description :
   Author :       hike
   time：          2021/4/28 15:47
"""
import pymssql
from dbutils.pooled_db import PooledDB
pool=PooledDB(
    creator=pymssql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    ping=0,
    port=39999,
    host='223.223.180.9',
    user='tuser1',
    password='tsuser1@123aA',
    database='QBB_B'
)

conn=pool.connection()
cursor_QBBB=conn.cursor()
sql="select * from TS_track_task where is_done=0"
cursor_QBBB.execute(sql)
datas=cursor_QBBB.fetchall()

for d in iter(datas):
    print(d)