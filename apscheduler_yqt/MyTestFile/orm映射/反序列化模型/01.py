#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/26 10:37
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import os
ret = os.popen(
    "sqlacodegen --noviews --noconstraints --noindexes "
    "--tables[TS_industry_news_circulation]  mssql+pymssql://sa:33221100@aA@223.223.180.9:39999/QBB_B"
)
print(ret.read())