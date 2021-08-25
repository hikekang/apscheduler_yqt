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

# 声明交换机
channel.exchange_declare(exchange='logs',exchange_type='fanout')#fanout 发布订阅模式

result=channel.queue_declare("",exclusive=True)
queue_name=result.method.queue
print(queue_name)

# 将指定队列绑定到交换机上
channel.queue_bind(exchange='logs',queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # 手动应答，效率会降低
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=queue_name,
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
