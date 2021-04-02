# -*- coding: utf-8 -*-
"""
   File Name：     myapscheduler
   Description :
   Author :       hike
   time：          2021/3/30 15:15
"""
import time

from apscheduler.schedulers.background import  BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

sched = BlockingScheduler()
def my_job():
	print(1)

def my_job1():
    print('my_job, {}'.format(time.ctime()))
#表示每隔3天17时19分07秒执行一次任务
# sched.add_job(my_job, 'interval',days=0,minutes = 0,seconds = 7)

trigger1 = CronTrigger(hour='9-18', minute='*/1',second=5, jitter=30)

sched.add_job(my_job1,trigger1,id='my_job_id')
sched.start()