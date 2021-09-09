# -*- coding: utf-8 -*-
"""
   File Name：     msq
   Description :
   Author :       hike
   time：          2021/4/16 16:44
"""
import stomp
from stomp import PrintingListener
def send_to_queue(queue_name,msg):
    conn1 = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)],auto_content_length=False)
    conn1.set_listener('', PrintingListener())
    conn1.connect('admin', 'admin')
    conn1.send(queue_name, msg,headers={'persistent':'true'})
    conn1.disconnect()

send_to_queue('asssss','dnaisda')