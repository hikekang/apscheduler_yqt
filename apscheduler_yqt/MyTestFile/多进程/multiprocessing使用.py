# -*- coding: utf-8 -*-
"""
   File Name：     multiprocessing使用
   Description :
   Author :       hike
   time：          2021/4/25 11:28
"""
import os
from multiprocessing import Process
from time import sleep
import subprocess
def task1():
    # while True:
    #     print('这是任务1\tPID：', os.getpid(), '\t父进程PPID：', os.getppid())
    #     print("\n")
    # os.system(r"java -jar F:\项目\sina_yuqing\apscheduler_yqt\yuqingtong\jms-1.1.1.jar")
    command=r"java -jar F:\项目\sina_yuqing\apscheduler_yqt\yuqingtong\jms-1.1.1.jar"
    # ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
    # while True:
    #     print(ret)
    os.system(command)
    print("执行成功")


def task2():
    # while True:
    #     sleep(1)
    #     print('这是任务2\tPID：', os.getpid(), '\t父进程PPID：', os.getppid())
    #     print("\n")
    print("hike")
if __name__ == '__main__':
    p1=Process(target=task1,name="任务1")
    p2=Process(target=task2,name="任务2")
    p1.start()
    p2.start()
    # p1.run()
    # p2.run()