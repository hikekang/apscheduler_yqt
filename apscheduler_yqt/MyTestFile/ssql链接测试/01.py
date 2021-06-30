# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/4/29 17:26
"""
import pymssql
connect_net_QBB_A = pymssql.connect(server='192.168.0.77', user='sa', password='33221100@aA', database='QBB_A',
                                    port='1433', autocommit=True)
cursor_QBBB = connect_net_QBB_A.cursor()