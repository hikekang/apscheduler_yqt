# -*- coding: utf-8 -*-
"""
   File Name：     apscheduler4
   Description :
   Author :       hike
   time：          2021/3/30 14:50
"""
import time
import datetime
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.date import DateTrigger


def my_job():
    print('my_job, {}'.format(time.ctime()))


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    intervalTrigger=DateTrigger(run_date='2021-03-30 14:50:55')
    scheduler.add_job(my_job, intervalTrigger, id='my_job_id')
    scheduler.start()
