#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/21 15:02
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : my_crontrigger.py
 Description:
 Software   : PyCharm
"""
from apscheduler.triggers.cron import CronTrigger
class my_CronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                    year=values[5], timezone=timezone)
