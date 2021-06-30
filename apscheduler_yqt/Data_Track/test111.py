# -*- coding: utf-8 -*-
"""
   File Name：     test111
   Description :
   Author :       hike
   time：          2021/4/16 14:28
"""
import time
import stomp

def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.send('/queue/test','hike')
    conn.subscribe(destination='/queue/test', id=1, ack='auto')

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        for x in range(10):
            print(x)
            time.sleep(1)
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)

conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
time.sleep(60)
conn.disconnect()