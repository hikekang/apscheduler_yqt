# -*- coding: utf-8 -*-
"""
   File Name：     pyodbc_test
   Description :
   Author :       hike
   time：          2021/4/30 11:16
"""
import pyodbc

# Database server information

# driver = 'ODBC Driver 17 for SQL Server'  # varies by version
# server =  '223.223.180.9',
# user = 'tuser1',
# password = 'tsuser1@123aA',
# database = 'QBB_B'
# conn = pyodbc.connect(driver=driver, server=server, user=user, password=password, database=database)
#
# cursor_QBBB = conn.cursor()


import pyodbc
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

server = '223.223.180.9.39999',
database = 'QBB_B'
username = 'tuser1',
password = 'tsuser1@123aA',
str='DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(server,database,username,password)
# str='DRIVER={ODBC Driver 13.1 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(server,database,username,password)
print(str)
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=223.223.180.9.39999;DATABASE=QBB_B;UID=tuser1;PWD=tsuser1@123aA')
cursor = cnxn.cursor()

sql="select * from TS_track_task where is_done=0"
cursor.execute(sql)
datas=cursor.fetchall()
for d in datas:
    print(d)