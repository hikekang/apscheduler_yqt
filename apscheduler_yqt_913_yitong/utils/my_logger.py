# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:31
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : my_logger.py


import os
import time
import logging


def get_logger(file_path, logger_name):

    os.makedirs(os.path.dirname(file_path),exist_ok=True)

    logger1 = logging.getLogger(logger_name)
    fh = logging.FileHandler(file_path)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger1.setLevel(logging.DEBUG)

    logger1.addHandler(fh)
    logger1.addHandler(ch)
    return logger1
