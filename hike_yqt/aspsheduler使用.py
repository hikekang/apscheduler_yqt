# -*- coding: utf-8 -*-
"""
   File Name：     aspsheduler使用
   Description :
   Author :       hike
   time：          2021/3/30 14:39
"""
from datetime import date

from apscheduler.schedulers.blocking import BlockingScheduler    # 引入模块
import os

def task():
    '''定时任务'''
    os.system('python3 spider.py')


if __name__ == '__main__':
    scheduler = BlockingScheduler()

    # 添加任务
    scheduler.add_job(task, 'cron', hour=11, minute=30)
    # 在2020-1-3这一天的凌晨执行task函数
    scheduler.add_job(task, 'date', run_date=date(2020, 1, 3))

    # 在1990-12-22 14:30:22时执行task函数
    scheduler.add_job(task, 'date', run_date='1990-12-22 14:30:22')

    # 未指定时间，则会立即执行
    scheduler.add_job(task, 'date')
    # 每隔1周3天8时20分5秒执行一次task函数
    scheduler.add_job(task, 'interval', weeks=1, days=3, hours=8, minutes=20, seconds=5)

    # 每天8时20分执行一次task函数
    scheduler.add_job(task, 'cron', hour=8, minute=20)

    # 从星期一到星期五的每一天8:20执行一次task函数，直到2100-05-20程序终止
    scheduler.add_job(task, 'cron', day_of_week='mon-fri', hour=8, minute=20, end_date='2100-05-20')

    scheduler.start()