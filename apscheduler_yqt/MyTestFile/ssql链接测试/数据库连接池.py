# -*- coding: utf-8 -*-
"""
   File Name：     数据库连接池
   Description :
   Author :       hike
   time：          2021/5/7 10:09
"""
import importlib

from dbutils.pooled_db import PooledDB
import pymssql

"""
1. mincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
2. maxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
3. maxconnections，最大的连接数，
4. blocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错，
5. maxshared 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
"""
pool = PooledDB(
    # 使用链接数据库的模块
    creator=pymssql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=0,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # 主机地址
    host='223.223.180.9',
    # 端口
    port=39999,
    # 数据库用户名
    user='tsuer1',
    # 数据库密码
    password='tsuser1@123aA',
    # 数据库名
    database='TS_A',
    # 字符编码
    charset='utf8',
    autocommit=True
)
config_A = {
    'creator': pymssql,
    'maxconnections': 6,
    'mincached': 2,
    'maxcached': 5,
    'maxshared': 3,
    'blocking': True,
    'maxusage': None,
    'host': '223.223.180.9',
    'user': 'tuser1',
    'password': 'tsuser1@123aA',
    'database': 'TS_A',
    'port': '39999',
    'charset': 'utf8',
    'autocommit': True
}


conn=pool.connection()
cur=conn.cursor()
sql="select * from crawler_word"
cur.execute(sql)
data=cur.fetchall()
for d in data:
    print(data)

class DataBase(object):

    def __init__(self, db_type, config):

        self.__db_type = db_type

        if self.__db_type == 'mysql':
            db_creator = importlib.import_module('pymysql')
        elif self.__db_type == 'sqlserver':
            db_creator = importlib.import_module('pymssql')
        elif self.__db_type == 'oracle':
            db_creator = importlib.import_module('cx_Oracle')
        else:
            raise Exception('unsupported database type ' + self.__db_type)
        self.pool = PooledDB(
            creator=db_creator,
            mincached=0,
            maxcached=6,
            maxconnections=0,
            blocking=True,
            ping=0,
            **config
        )

    def execute_query(self, sql, as_dict=False):
        """
        查询语句
        :param sql:
        :param as_dict:
        :return:
        """
        conn = None
        cur = None
        try:
            conn = self.pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            rst = cur.fetchall()
            if rst:
                if as_dict:
                    fields = [tup[0] for tup in cur._cursor.description]
                    return [dict(zip(fields, row)) for row in rst]
                return rst
            return rst

        except Exception as e:
            print('sql:[{}]meet error'.format(sql))
            print(e.args[-1])
            return ()
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()

    def execute_manay(self, sql, data):
        """
        执行多条语句
        :param sql:
        :param data:
        :return:
        """
        conn = None
        cur = None
        try:
            conn = self.pool.connection()
            cur = conn.cursor()
            cur.executemany(sql, data)
            conn.commit()
            return True
        except Exception as e:
            print('[{}]meet error'.format(sql))
            print(e.args[-1])
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()


db_A = DataBase(
    'sqlserver', {'host': '192.168.0.77',
    'user': 'sa',
    'password': '33221100@aA',
    'database': 'TS_A',
    'port': '1433',
    'charset': 'utf8',
    'autocommit': True}
)
for d in db_A.execute_query("select * from TS_test"):
    print(d)
