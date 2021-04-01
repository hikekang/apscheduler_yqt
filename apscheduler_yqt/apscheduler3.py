# -*- coding: utf-8 -*-
"""
   File Name：     apscheduler
   Description :
   Author :       hike
   time：          2021/3/30 14:48
"""
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# BackgroundScheduler它可以在后台运行，不会阻塞主线程的执行，来看下面的代码
def my_job():
    print('my_job, {}'.format(time.ctime()))


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    intervalTrigger=IntervalTrigger(seconds=1)
    scheduler.add_job(my_job, intervalTrigger, id='my_job_id')
    # 表示每隔3天17时19分07秒执行一次任务
    scheduler.add_job(my_job, 'interval', days=3, hours=17, minutes=19)


    scheduler.start()
    print('=== end. ===')
    while True:
        time.sleep(1)