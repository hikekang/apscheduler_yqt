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
import pickle
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body,*args):
    print(args)
    # print(" [x] Received %r" % body)
    str_body=eval(body.decode('utf-8'))
    # print("body的数据类型为：",type(body))
    print("str_body的数据类型为：",type(str_body))
    print("str_body：",str_body)
    print(str_body['test'])
    print(type(str_body['test']))

    # data=pickle.loads(body)
    # print(type(data))
    # print(data)
    # 手动应答，效率会降低
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='hello',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=callback,arguments={"name":"123"})


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
