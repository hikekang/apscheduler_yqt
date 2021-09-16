# _*_coding:utf-8 _*_
# @Time　　:2021/9/10   10:09
# @Author　 : Antipa
# @ File　　  :02get_data_from_weibo.py
# @Software  :PyCharm
# @Description
import pika
from datetime import datetime
from utils.ssql_helper_test import db_qbbb
from utils.sedn_msg import send_feishu_msg
from get_data_by_selenium import get_num_driver
from get_data_by_requests import get_data_item
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
queue_name_2='ts_track_spider'
channel.queue_declare(queue=queue_name_2,durable=True)

def track_data_task_by_selenim(ch,method,properties,body):
    """
    直接扫描表
    数据库中获取链接进行追踪
    """

    data = eval(body.decode('utf-8'))
    # for data in url_data:
    driver = get_num_driver()
    num = driver.get_data_it(data[1])
    print(data)


    print("关闭浏览器")
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     转发、评论、点赞
    # 追踪记录
    sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
        data[0], num[0], num[1], num[2], create_date)
    db_qbbb.execute(sql_record)
    # 更新值
    sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
        num[0], num[1], num[2], data[0])
    db_qbbb.execute(sql_Base)
    print('更新库')
    #     修改数据追踪表
    # sql_track_task = "update TS_track_task set is_done=1 where sn='%s' " % data[0]
    # db_qbbb.execute(sql_track_task)
        # print('追踪完毕')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def track_data_task_by_request(ch,method,properties,body):
    """
    直接扫描表
    数据库中获取链接进行追踪
    """

    data = eval(body.decode('utf-8'))
    # for data in url_data:
    num=get_data_item(data[1])
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     转发、评论、点赞
    # 追踪记录
    sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
        data[0], num[0], num[1], num[2], create_date)
    db_qbbb.execute(sql_record)
    # 更新值
    sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
        num[0], num[1], num[2], data[0])
    db_qbbb.execute(sql_Base)
    print('更新库')
    #     修改数据追踪表
    # sql_track_task = "update TS_track_task set is_done=1 where sn='%s' " % data[0]
    # db_qbbb.execute(sql_track_task)
        # print('追踪完毕')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name,
    auto_ack=False,
    on_message_callback=track_data_task_by_request
)
channel.start_consuming()