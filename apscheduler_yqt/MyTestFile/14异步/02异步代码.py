#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/14 16:33
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 异步代码.py
 Description:
 Software   : PyCharm
"""
# import time
# import asyncio
#
# # 定义异步函数
# async def turn_page():
#     for i in range(5):
#         page_data=parse_data(i)
#         cleardata=clear_data(page_data)
#         await upload(cleardata)
#
# def parse_data(i):
#     print("获取第%s页数据"%i)
#     time.sleep(3)
#     return "第%s页数据"%i
#
# def clear_data(data):
#     print("清洗数据")
#     return data+"清洗数据"
# async def upload(data):
#     print("上传数据")
#     time.sleep(10)
#     return data+"上传"
#
#
#
#
# if __name__ =='__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(turn_page())


# import asyncio
# import time
#
# #定义第1个协程，协程就是将要具体完成的任务，该任务耗时3秒，完成后显示任务完成
# async def to_do_something(i):
#     print('第{}个任务：任务启动...'.format(i))
#     #遇到耗时的操作，await就会使任务挂起，继续去完成下一个任务
#     await asyncio.sleep(i)
#     print('第{}个任务：任务完成！'.format(i))
#     return i
# #定义第2个协程，用于通知任务进行状态
# async def mission_running():
#     print('任务正在执行...')
#
# start = time.time()
# #创建一个循环
# loop = asyncio.get_event_loop()
# #创建一个任务盒子tasks，包含了3个需要完成的任务
# tasks = [asyncio.ensure_future(to_do_something(1)),
#          asyncio.ensure_future(to_do_something(2)),
#          asyncio.ensure_future(mission_running())]
# #tasks接入loop中开始运行
# loop.run_until_complete(asyncio.wait(tasks))
# end = time.time()
#
# print(tasks[1].result())
# print(end-start)


import requests
import asyncio
import time
async def test2(i):
    r = await other_test(i)
    print(i,r)

async def other_test(i):
    r = requests.get(i)
    print(i)
    await asyncio.sleep(4)
    print(time.time()-start)
    return r

url = ["https://segmentfault.com/p/1210000013564725",
   "https://www.jianshu.com/p/83badc8028bd",
    "https://www.baidu.com/"]

loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(test2(i)) for i in url]
start = time.time()
loop.run_until_complete(asyncio.wait(task))
endtime = time.time()-start
print(endtime)
loop.close()
