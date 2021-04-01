# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 12:35
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : mylogger.py
import logging
from logging.handlers import RotatingFileHandler
import os

logger = logging.getLogger()
# print(type(logger))
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
# print(__name__)
# fh = logging.FileHandler('./log/test2.log', encoding="utf-8")
fh = RotatingFileHandler('../log/test.log', mode='a', maxBytes=5 * 1024 * 1024, backupCount=2, delay=0, encoding="utf-8")

fh.setLevel(logging.INFO)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(filename)s[line:%(lineno)d] - %(levelname)s - %(asctime)s - %(message)s',
                              datefmt="%Y-%m-%d %H:%M:%S")

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)  # logger对象可以添加多个fh和ch对象
logger.addHandler(ch)


class MyLogger(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    logger.debug('logger debug message')
    logger.info('logger info message')
    logger.warning('logger warning message')
    logger.error('logger error message')
    logger.critical('logger critical message')
