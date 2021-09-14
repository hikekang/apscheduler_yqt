# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 12:35
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : mylogger.py
import logging
from logging.handlers import RotatingFileHandler
import os
# 使用RotatingFileHandler，可以实现日志回滚
logger = logging.getLogger()
# print(type(logger))

# 设置日志级别
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
dir_path = os.path.dirname(os.getcwd())
dir_path=os.path.join(dir_path,'log')
log_path = os.path.join(dir_path, 'test.log')
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
    print("创建成功")
if not os.path.exists(log_path):
    with open(log_path,"wb") as f:
        f.close()

# 最多备份3个日志文件，每个日志文件最大8*1024*1024 bit
fh = RotatingFileHandler('../log/test1.log', mode='a', maxBytes=8 * 1024 * 1024, backupCount=5, delay=0, encoding="utf-8")

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
"""
日志等级：使用范围
 
FATAL：致命错误
CRITICAL：特别糟糕的事情，如内存耗尽、磁盘空间为空，一般很少使用
ERROR：发生错误时，如IO操作失败或者连接问题
WARNING：发生很重要的事件，但是并不是错误时，如用户登录密码错误
INFO：处理请求或者状态变化等日常事务
DEBUG：调试过程中使用DEBUG等级，如算法中每个循环的中间状态

"""

if __name__ == '__main__':
    # logger.debug('logger debug message')
    # logger.info('logger info message')
    # logger.warning('logger warning message')
    # logger.error('logger error message')
    # logger.critical('logger critical message')
    print(1)
