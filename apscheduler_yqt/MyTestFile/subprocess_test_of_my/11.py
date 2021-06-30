# -*- coding: utf-8 -*-
"""
   File Name：     11
   Description :
   Author :       hike
   time：          2021/4/21 11:48
"""
import subprocess
command=r'java -jar jms-1.0.0.jar'
# stdout, stderr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
# print(stdout,stderr)
command1=r'ping www.baidu.com -t'
subprocess.run(command1)

print('hike')
import  os
# os.system('run.bat')
print('hike')
print("我是")