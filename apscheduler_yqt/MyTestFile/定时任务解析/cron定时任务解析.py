#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/21 10:35
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : cron定时任务解析.py
 Description:
 Software   : PyCharm
"""
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
def test():
    print("测试")
    print(datetime.now())
cron_1="*/3 * * * *  "
cron_1="*/1 * * * * * *"

class my_CronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


c1=my_CronTrigger.my_from_crontab(cron_1)
sched=BlockingScheduler()
sched.add_job(test,c1,max_instances=10,id="hike")
sched.start()