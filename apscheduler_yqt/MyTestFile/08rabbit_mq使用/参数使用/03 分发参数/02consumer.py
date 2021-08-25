#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/6 10:58
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : consumer.py
 Description:
 Software   : PyCharm
"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello4',durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # 手动应答，效率会降低
    import time
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 公平分发
channel.basic_qos(prefetch_count=1)
# for i in range(10):
channel.basic_consume(queue='hello4',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,  # 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=callback,

                      )
channel.start_consuming()

