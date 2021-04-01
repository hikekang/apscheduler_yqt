# -*- coding: utf-8 -*-

from yuqingtong.yqt_spider import YQTSpider
from yuqingtong import config

# time_list=config.get_time_list()
if __name__ == '__main__':
    time_list=config.get_time_list()
    cishu = 1
    print(len(time_list))
    for tim in time_list:
        yqt_spider = YQTSpider(start_time=tim['start_time'], end_time=tim['end_time'])
        yqt_spider.start(start_time=tim['start_time'], end_time=tim['end_time'], time_sleep=tim['time_delay'])
        config.info['start_time'] = tim['start_time']
        config.info['end_time'] = tim['end_time']
