# _*_coding:utf-8 _*_
# @Time　　:2021/9/10   9:46
# @Author　 : Antipa
# @ File　　  :01get_track_url.py
# @Software  :PyCharm
# @Description
import re
import pika
import traceback
from datetime import datetime
from utils.sedn_msg import send_feishu_msg
from utils.ssql_helper_test import db_qbbb
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
pika_username="ts_track"
pika_pwd="123456"
host='/ts_track'
credentials=pika.PlainCredentials(pika_username,pika_pwd)
connection=pika.BlockingConnection(
    pika.ConnectionParameters(
        host="127.0.0.1",
        port=5672,
        virtual_host=host,
        credentials=credentials,
        heartbeat=0
    )
)
channel=connection.channel()
queue_name='ts_track_list'
channel.queue_declare(queue=queue_name,durable=True)

def get_track_url_qbbb():
    """
    从TS_track_task中获取追踪数据
    数据库qbbb,track_task中获取数据
    """
    try:
        sql="select sn from TS_DataMerge_Extend with(NOLOCK) where is_Track=1"
        datas_extend_track=db_qbbb.execute_query(sql)
        data_track_list=[]
        if datas_extend_track:
            for item in datas_extend_track:
                sql_base=f"select sn,url from TS_DataMerge_Base with(NOLOCK) where sn='{item[0]}'"
                base_result=db_qbbb.execute_query(sql_base)
                if base_result:
                    data_track_list.append(base_result[0])

        channel.basic_qos(prefetch_count=1)
        for data in data_track_list:
            print(data)
            pattern = re.compile(r'http://weibo.com.*')
            reslut=re.findall(pattern,data[1])
            if reslut:
                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=str(data),
                    properties=pika.BasicProperties(
                        delivery_mode=2
                    )
                )
                print("数据传送完毕")
    except:
        send_feishu_msg(traceback.format_exc())

def apscheduler_task():
    hour_trigger=CronTrigger.from_crontab("01 * * * *")
    schedule=BlockingScheduler()
    schedule.add_job(get_track_url_qbbb,trigger=hour_trigger,max_instances=20,id="get_url")
    schedule.start()

if __name__ == '__main__':
    # for item in  get_track_url_qbbb():
    #     print(item)
    get_track_url_qbbb()

