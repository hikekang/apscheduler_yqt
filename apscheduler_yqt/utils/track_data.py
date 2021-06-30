#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:41
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : track_data.py
# @Software: PyCharm
import stomp
import re
import time
from datetime import datetime
from utils.getdatabyselenium import get_num_driver
from utils.ssql_helper_test import db_qbbb


"""

数据追踪
"""
class TrackDataByTable():
    """
    直接在表中获取
    外加一个apscheduler任务

    """
    def __init__(self,db_qbb):
        self.db_qbb=db_qbb

    def get_track_datas_qbbb(self):
        """
        数据库qbbb,track_task中获取数据
        """
        sql="select * from TS_track_task where is_done=0"
        self.db_qbb.execute(sql)
        datas=self.db_qbb.execute_query()
        return datas

    def track_data_task(self):
        """
        直接扫描表
        数据库中获取链接进行追踪
        """
        driver=get_num_driver()
        for data in self.get_track_datas_qbbb():

            num = driver.get_data_it(data[1])
            create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #     转发、评论、点赞
            # 追踪记录
            sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
            data[2], num[0], num[1], num[2], create_date)
            self.db_qbbb.execute(sql_record)
            # 更新值
            sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
            num[0], num[1], num[2], data[2])
            self.db_qbbb.execute(sql_Base)
            # print('更新库')
             #     修改数据追踪表
            sql_track_task="update TS_track_task set is_done=1 where sn='%s' "%data[2]
            self.db_qbbb.execute(sql_track_task)
            # print('追踪完毕')
        driver.close()

        def get_track_url(self):
            """
            数据库中获取追踪的url
            """
            sql_of_extend = "select SN from TS_DataMerge_Extend where is_Track=1"
            datas = self.db_qbb.execute_query(sql_of_extend)
            url_list = []
            for data in datas:
                sql_of_base = "select URL from TS_DataMerge_Base where SN='%s'" % (data[0])
                urls = self.db_qbb.execute_query(sql_of_base)
                if "weibo.com" in urls[0]:
                    url = {
                        'sn': data[0],
                        'url': urls[0]
                    }
                    url_list.append(url)
            return url_list


def track_data_number_sql2(sn, data):
    """
    stomp版本
    将得到的数据插入数据库
    """
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     转发、评论、点赞
    sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
    sn, data[0], data[1], data[2], create_date)
    db_qbbb.execute(sql_record)
    sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
    data[0], data[1], data[2], sn)
    db_qbbb.execute(sql_Base)


# ----------------------------数据追踪消息队列------------------------------------------------

class MyListener(stomp.ConnectionListener):
    """
    自己的监听队列，操作数据库
    """
    def __init__(self,conn):
        self.conn = conn
        self.msg_list=[]

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        if frame.body!=None:
            get_url_from_stomp(frame.body)
    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)
    def get_msg_list(self):
        print(self.msg_list)
        return self.msg_list

def connect_and_subscribe(conn):
    """
    连接和监听
    """
    conn.connect('admin', 'admin', wait=True)
    # conn.send(destination='aahike',body="hike")
    # conn.subscribe(destination='aahike', id=1, ack='auto')
    conn.subscribe(destination='task.msg.tracker', id=1, ack='auto')
    # conn.subscribe(destination='task.msg.tracker_2.1', id=1, ack='auto')


def re_connect_subscribe(conn):
    """
    重新登记注册
    :return:
    """
    conn.disconnect()
    time.sleep(3)
    connect_and_subscribe(conn)

def get_url_from_stomp_list(frame_body_list):
    try:
        if frame_body_list:
            print("开始抓数据")
            for frame_body in frame_body_list:
                pattern = re.compile(r'http://weibo.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                url = re.findall(pattern, frame_body)
                driver=get_num_driver()
                data = driver.get_data_it(url[0])
                sn = frame_body.split('"')[3]
                track_data_number_sql2(sn, data)
                for x in range(3):
                    print(x)
                    time.sleep(1)
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        driver.close()

def get_url_from_stomp(frame_body):
    try:
        print("frame_body",frame_body)
        pattern = re.compile(r'http://weibo.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        url = re.findall(pattern, frame_body)
        print("url",url)
        if url:
            driver=get_num_driver()
            data = driver.get_data_it(url[0])
            sn = frame_body.split('"')[3]
            track_data_number_sql2(sn, data)
            for x in range(3):
                print(x)
                time.sleep(1)
            return True
    except Exception as e:
        print("异常",e)
        return False
def track_data_work():
    conn = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)],heartbeats=(4000, 4000))
    lst = MyListener(conn)
    conn.set_listener('track_data', lst)
    connect_and_subscribe(conn)
    i = 0
    while 1:
        i += 1
        time.sleep(10)
        if i == 18:
            re_connect_subscribe(conn)
            i = 0
if __name__ == '__main__':
    track_data_work()