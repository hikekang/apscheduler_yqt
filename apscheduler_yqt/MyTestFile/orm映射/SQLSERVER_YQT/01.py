#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/4 17:14
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import os
ret = os.popen(
    "sqlacodegen --noviews --noconstraints --noindexes --outfile=xx_model.py --tables TS_DataMerge_Base mssql+pymssql://user1:123456@223.223.180.9:39999/QBB_B "
)

"""
sqlacodegen mssql+pymssql://sql_username:sql_password@server/database > db_name.py
sqlacodegen --tables TS_DataMerge_Base mssql+pymssql://user1:123456@223.223.180.9:39999/QBB_B > db_name.py

"""



print(ret.read())