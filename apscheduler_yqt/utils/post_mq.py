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
    conn = stomp.Connection(host_and_ports=[('223.223.180.10',61613)])
    # conn = stomp.Connection(host_and_ports=[('127.0.0.1',61613)])
    # conn = stomp.Connection(host_and_ports=[('192.168.0.146',61613)])
    # conn.set_listener('', PrintingListener())
    conn.set_listener('', PrintingListener())
    conn.connect('admin', 'admin')
    conn.send(queue_name, msg,headers={'persistent':'true'})
    # conn.subscribe('/queue/a2',111111)
    conn.disconnect()


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
#  Transport Connection to: tcp://192.168.0.146:49708 failed: java.net.SocketException: Software caused connection abort: recv failed
def my_test_mq():
    conn = stomp.Connection([('223.223.180.10', 8161)])
    conn.set_listener('', PrintingListener())
    conn.connect(username='admin', passcode='admin')
    conn.send('hike','456')
    conn.disconnect()
    # 消息丢失
if __name__ == '__main__':
    data = {
        'id': "111111",'industry_id': "222222"
    }
    # send_to_queue('aaprocess2323232',str(data))
    for i in range(50):
        send_to_queue('a6',str(data))