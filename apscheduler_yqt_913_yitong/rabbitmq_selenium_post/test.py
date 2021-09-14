# _*_coding:utf-8 _*_
# @Time　　:2021/9/13   17:37
# @Author　 : Antipa
# @ File　　  :test.py
# @Software  :PyCharm
# @Description
import pika
from utils.ssql_pool_helper import DataBase,config_myQBB_A_net

db=DataBase('sqlserver',config_myQBB_A_net)

sql="select top(50) * from myQBB_A.dbo.TS_industry_news_automotive  order by publish_time desc  "

data_list=db.execute_query(sql)
