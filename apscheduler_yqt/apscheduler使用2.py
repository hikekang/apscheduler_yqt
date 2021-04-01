# -*- coding: utf-8 -*-
"""
   File Name：     apscheduler使用2
   Description :
   Author :       hike
   time：          2021/3/30 14:43
"""
import time
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


def my_job():
    print('my_job, {}'.format(time.ctime()))


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # 间隔设置为1秒，还可以使用minutes、hours、days、weeks等
    intervalTrigger=IntervalTrigger(seconds=1)

    # 给作业设个id，方便作业的后续操作，暂停、取消等
    scheduler.add_job(my_job, intervalTrigger, id='my_job_id')
    scheduler.start()
    print('=== end. ===')