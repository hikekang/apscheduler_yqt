# -*- coding: utf-8 -*-
"""
   File Name：     apscheduler5
   Description :
   Author :       hike
   time：          2021/3/30 14:52
"""
import time
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def my_job():
    print('my_job, {}'.format(time.ctime()))


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # 第一秒执行作业
    intervalTrigger=CronTrigger(second=1)

    # 每天的19:30:01执行作业
    # intervalTrigger=CronTrigger(hour=19, minute=30, second=1)

    # 每年的10月1日19点执行作业
    # intervalTrigger=CronTrigger(month=10, day=1, hour=19)
    from apscheduler.triggers.cron import CronTrigger

    # 高峰期，每天早九点到晚六点，每30分钟执行一次
    trigger1 = CronTrigger(hour='9-18',minute = '*/30',jitter = 30)
    # 低峰期，每天晚八点至第二天早上六点，每五分钟执行一次
    # trigger2 = CronTrigger(hour='20-23,0-5',minute = '*/5',jitter = 30)


    sched = BlockingScheduler()
    # 表示2017年3月22日17时19分07秒执行该程序
    sched.add_job(my_job, 'cron', year=2017, month=3, day=22, hour=17, minute=19, second=7)

    # 表示任务在6,7,8,11,12月份的第三个星期五的00:00,01:00,02:00,03:00 执行该程序
    sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

    # 表示从星期一到星期五5:30（AM）直到2014-05-30 00:00:00
    sched.add_job(my_job(), 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')

    # 表示每5秒执行该程序一次，相当于interval 间隔调度中seconds = 5
    sched.add_job(my_job, 'cron', minute='*/10',second='*/5')

    scheduler.add_job(my_job, intervalTrigger, id='my_job_id')
    scheduler.start()
