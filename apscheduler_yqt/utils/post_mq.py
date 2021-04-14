# -*- coding: utf-8 -*-
"""
   File Name：     post_mq
   Description :
   Author :       hike
   time：          2021/4/8 16:22
"""
# -*-coding:utf-8-*-
import sys

import stomp
import time
from stomp import PrintingListener

# queue_name = '/queue/SampleQueue'
topic_name = '/topic/SampleTopic'
listener_name = 'SampleListener'


class SampleListener(object):
    def on_message(self, headers, message):
        print('headers: %s' % headers)
        print('message: %s' % message)



# 推送到队列queue
def send_to_queue(queue_name,msg):
    conn1 = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)],auto_content_length=False)
    conn1.set_listener('', PrintingListener())
    conn1.connect('admin', 'admin')
    conn1.send(queue_name, msg,headers={'persistent':'true'})
    conn1.disconnect()


# 推送到主题
def send_to_topic(msg):
    conn = stomp.Connection10([('127.0.0.1', 61613)])
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.send(topic_name, msg)
    conn.disconnect()


##从队列接收消息
def receive_from_queue(queue_name):
    conn = stomp.Connection10([('127.0.0.1', 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(queue_name)
    time.sleep(1)  # secs
    conn.disconnect()


##从主题接收消息
def receive_from_topic():
    conn = stomp.Connection10([('127.0.0.1', 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(topic_name)
    while 1:
        send_to_topic('topic')
        time.sleep(3)  # secs

    conn.disconnect()
def my_test_mq():
    conn = stomp.Connection([('223.223.180.10', 8161)])
    conn.set_listener('', PrintingListener())
    conn.connect(username='admin', passcode='admin')
    conn.send('hike','456')
    conn.disconnect()
    # 消息丢失
if __name__ == '__main__':
    data = {"id":12,"industryId":9999}
    for i in range(100):
        send_to_queue('aaa',str(data))
        send_to_queue('reptile.stay.process_2.1',str(data))