# -*- coding: utf-8 -*-
"""
   File Name：     testmq
   Description :
   Author :       hike
   time：          2021/4/9 14:29
"""
import stomp
import time

class MyListener(object):
    msg_list = []

    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)
        # global rcvd_msg, lock
        # with lock:
        #     while rcvd_msg != None:
        #         lock.wait()
        #     rcvd_msg = message
        #     lock.notifyAll()

    def on_message(self, message):
        self.msg_list.append(message.body)
        print(message.body)
        print('执行on_message')


# class MyListener(stomp.ConnectionListener):
#     def __init__(self, conn):
#         self.conn = conn
#
#     def on_error(self, frame):
#         print('received an error "%s"' % frame.body)
#
#     def on_message(self, frame):
#         print('received a message "%s"' % frame.body)
#         for x in range(10):
#             print(x)
#             time.sleep(1)
#         print('processed message')
#
#     def on_disconnected(self):
#         print('disconnected')
import threading
# rcvd_msg = None
# lock = threading.Condition()

# executed in the main thread
# with lock:
#     while rcvd_msg == None:
#         lock.wait()
#     # read rcvd_msg
#     rcvd_msg = None
#     lock.notifyAll()

conn = stomp.Connection()
lst = MyListener()
conn.set_listener('', lst)
conn.connect()
for i in range(10):
    conn.send('/queue/test',str(i),headers={'persistent':'true'})


while 1:
    conn.subscribe(destination='/queue/test', id=1, ack='auto')
    time.sleep(1)
    # conn.unsubscribe(destination='/queue/test',id=2)



