# -*- coding: utf-8 -*-
"""
   File Name：     snowflake
   Description :
   Author :       hike
   time：          2021/4/8 15:47
"""
# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

import time
import logging

from utils.exceptions import InvalidSystemClock


# 64位ID的划分
WORKER_ID_BITS = 7
DATACENTER_ID_BITS = 6
SEQUENCE_BITS = 10

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
# print(MAX_WORKER_ID)
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1288834974657


logger = logging.getLogger('flask.app')


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            # print(worker_id)
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳
        self.id=set()

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        # time.sleep(0.001)
        return int(time.time()*1000)

    def get_id(self,i=None):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()
        # print(timestamp)

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        # n_id=int(str(new_id)[1:-1])
        # self.id.add(new_id)
        # print(n_id)
        # print(new_id)
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        等到下0.1秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

import threading
from multiprocessing.dummy import Pool as ThreadPool
if __name__ == '__main__':
    worker1 = IdWorker(1, 2, 0)
    worker2 = IdWorker(1, 3, 0)
    worker3 = IdWorker(2, 3, 1)
    print(worker1.get_id())
    print(worker2.get_id())
    print(worker3.get_id())

    # pool = ThreadPool()
    # pool.map(worker.get_id, range(500))
    # pool.close()
    # pool.join()

    # print(time.time())
    # for i in range(50):
    #     threading.Thread(target=worker.get_id).start()
    # id=674696343490031394880
    # str_id=str(id)[1:-1]
    # print(len(str_id))
    # print(str_id)
    # print(len(worker.id))
    # print(worker.id)
    # print(len(worker.id))
    # print(time.time())