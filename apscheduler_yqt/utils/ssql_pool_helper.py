# -*- coding: utf-8 -*-
"""
   File Name：     ssql_pool_helper
   Description :
   Author :       hike
   time：          2021/5/7 10:31
"""
import importlib
from dbutils.pooled_db import PooledDB
import pymssql
config_A = {
    'host': '223.223.180.9',
    'user': 'user1',
    'password': '123456',
    'database': 'TS_A',
    'port': '39999',
    'charset': 'utf8',
    'autocommit': True
}

config_B = {
    'host': '223.223.180.9',
    'user': 'user1',
    'password': '123456',
    'database': 'TS_B2.0',
    'port': '39999',
    'charset': 'utf8',
    'autocommit': True
}
config_QBBA = {
    'host': '223.223.180.9',
    'user': 'user1',
    'password': '123456',
    'database': 'QBB_A',
    'port': '39999',
    'charset': 'utf8',
    'autocommit': True
}
config_QBBB = {
    'host': '223.223.180.9',
    'user': 'user1',
    'password': '123456',
    'database': 'QBB_B',
    'port': '39999',
    'charset': 'utf8',
    'autocommit': True
}
config_net_QBBA = {
    'host': '192.168.0.77',
    'user': 'sa',
    'password': '33221100@aA',
    'database': 'QBB_A',
    'port': '1433',
    'charset': 'utf8',
    'autocommit': True
}
config_net_TS_A = {
    'host': '192.168.0.77',
    'user': 'sa',
    'password': '33221100@aA',
    'database': 'TS_A',
    'port': '1433',
    'charset': 'utf8',
    'autocommit': True
}
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
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()

    def execute_many(self, sql, data):
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
            print("执行sql成功")
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
    def execute(self, sql,data=None):
        """
        执行单条语句
        :param sql:
        :param data:
        :return:
        """
        conn = None
        cur = None
        try:
            conn = self.pool.connection()
            cur = conn.cursor()
            if data:
                cur.execute(sql,data)
            else:
                cur.execute(sql)
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

if __name__ == '__main__':
    db=DataBase('sqlserver',config_A)
    db.execute_query("select * from crawler_word")
    # str=b"\xe7\x94\xa8\xe6\x88\xb7 'user1' \xe7\x99\xbb\xe5\xbd\x95\xe5\xa4\xb1\xe8\xb4\xa5\xe3\x80\x82DB-Lib error message 20018, severity 14:\nGeneral SQL Server error: Check messages from the SQL Server\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (223.223.180.9)\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (223.223.180.9)\n"
    # print(str.decode('utf-8'))