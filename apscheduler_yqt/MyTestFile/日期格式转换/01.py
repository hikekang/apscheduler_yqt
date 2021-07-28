# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/5/7 15:32
"""
import datetime
t1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(t1.date())
t2=datetime.datetime.strptime('2021-07-28 17:13:57','%Y-%m-%d %H:%M:%S')
print(t2)
print(type(t2))
time1 = (t2 - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
print(type(time1))
print(time1)
#
# sql_industry_num = """
#     if not exists (select * from record_log_table_industry  where industry = {0} and record_time={1})
#             INSERT INTO record_log_table_industry (industry,record_time,yqt_num,upload_num,first_data_num,redis_num) VALUES ({0},{1},{2},{3},{4},{5})
#         else
#             UPDATE record_log_table_industry SET record_time={1},yqt_num={2},upload_num={3},first_data_num={4},redis_num={5}
#
#            WHERE industry = {0} and record_time={1}
#     """.format('data[0]', 'today', 'data[4]',' data[5]',' data[7]', 'data[8]')
#
# print(sql_industry_num)
# aa='\xe6\xb5\x81\xe9\x80\x9a\xe8\xb4\xb8\xe6\x98\x93'
# print(aa.encode('raw_unicode_escape').decode())