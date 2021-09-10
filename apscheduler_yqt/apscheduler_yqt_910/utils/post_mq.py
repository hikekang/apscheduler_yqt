# -*- coding: utf-8 -*-
"""
   File Name：     post_mq
   Description :
   Author :       hike
   time：          2021/4/8 16:22
"""
# -*-coding:utf-8-*-
import stomp
from stomp import PrintingListener
# from utils.ssql_helper import track_data_number_sql2
# 推送到队列queue
conn1 = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)],auto_content_length=False)
conn1.set_listener('', PrintingListener())
conn1.connect('admin', 'admin')

def send_to_queue(queue_name,msg):
    conn1 = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)], auto_content_length=False)
    conn1.set_listener('', PrintingListener())
    conn1.connect('admin', 'admin')
    conn1.send(queue_name, msg,headers={'persistent':'true'})

def close_mq():
    conn1.disconnect()


def content_send_close(queue_name,msg):
    conn1 = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)], auto_content_length=False)
    conn1.set_listener('', PrintingListener())
    conn1.connect('admin', 'admin')
    conn1.send(queue_name, msg, headers={'persistent': 'true'})
    conn1.disconnect()



#
# for i in range(1,100):
#     send_to_queue("hike",str(i))
# conn.disconnect()