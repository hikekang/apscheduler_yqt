import pymssql
import threading
from dbutils.pooled_db import PooledDB

import greenlet

POOL = PooledDB(
    creator=pymssql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    ping=0,
    # ping MySQL服务端，检查是否服务可用。
    # 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

    port=1433,
    # charset='cp936',
    # charset='cp936',

    host='223.223.180.9',
    user='tuser1',
    password='tsuser1@123aA',
    database='TS_A',

    # host='123.56.250.57',
    # user='social',
    # password='moonshine**1',
    # database='Social360_A',

    # host='123.56.45.19',
    # user='social',
    # password='moonshine**1',
    # database='Social360_Config',

)


class SqlHelper(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        conn = POOL.connection()
        cursor = conn.cursor()

        return conn, cursor

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def __enter__(self):
        self.conn, self.cursor = self.open()
        return self.cursor,self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(self.cursor, self.conn)


def task(i):
    sql = "select * from crawler_word;"
    with SqlHelper() as cur:
        cur.execute(sql)
        data = cur.fetchall()
        print(i, data)


if __name__ == '__main__':
    task(1)
