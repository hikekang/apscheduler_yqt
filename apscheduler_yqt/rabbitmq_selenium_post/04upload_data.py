#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/12 17:19
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 04upload_data.py
 Description:
 Software   : PyCharm
"""
import pika
from utils.mylogger import logger
# from utils import ssql_helper_test as ssql_helper
from utils import qinbaobing_ssql as ssql_helper
from utils.sedn_msg import send_feishu_msg
credentials=pika.PlainCredentials('qb_04','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1',port=5672,virtual_host='/',credentials=credentials,heartbeat=600))
channel = connection.channel()
# channel.queue_declare(queue='qb_clear_data',durable=True)
channel.queue_declare(queue='qb_upload_data',durable=True)

def upload_data(ch, method, properties, body):
    """
    解析数据
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """

    str_body = eval(body.decode('utf-8'))
    # print(str_body)

    #将源码传入抓取队列，进行抓取
    logger.info("进行抓取解析")
    ssql_helper.upload_many_data(str_body['data'],str_body['info']['industry_name'],str_body['datacenter_id'],str_body['info'])
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.info("上传到数据库异常")
        send_feishu_msg("上传数据库异常")
    # 手动应答，效率会降低

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='qb_upload_data',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,
                      on_message_callback=upload_data)

print("Start_consuming")
channel.start_consuming()