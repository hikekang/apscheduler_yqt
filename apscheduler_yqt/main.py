# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import yuqingtong.yqt_spider as yq

# time_list=config.get_time_list()
if __name__ == '__main__':
    trigger1 = CronTrigger(hour='9-18', minute='*/', second=0, jitter=30)
    sched = BlockingScheduler()
    sched.add_job(yq.work_it, trigger1, id='my_job_id')
    sched.start()