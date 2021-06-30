# -*- coding: utf-8 -*-
"""
   File Name：     test_crontrigger
   Description :
   Author :       hike
   time：          2021/4/22 11:05
"""
import apscheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
trigger=CronTrigger(second='*/10')
sched=BlockingScheduler()
def my():
    print('hike')
# sched.add_job(my,trigger,id='my')
# sched.start()

import datetime
end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
start_time = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

print(type(start_time),end_time)