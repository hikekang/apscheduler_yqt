# -*- coding: utf-8 -*-
"""
   File Name：     11
   Description :
   Author :       hike
   time：          2021/4/22 16:13
"""

import threading
from time import sleep,time
from selenium import webdriver
from multiprocessing import current_process


def user_login(username,password):
    """
    单终端多线程登录
    :param username:
    :param password:
    :return:
    """
    url = "https://account.cnblogs.com/signin"
    driver = webdriver.Chrome()
    procName = current_process().name
    print("当前进程:",procName)
    sleep(1)
    start = time()
    print("session_id: " + driver.session_id)
    try:
        driver.get(url)
        driver.maximize_window()
        driver.find_element_by_id("LoginName").send_keys(username)
        sleep(1.5)
        driver.find_element_by_id("Password").send_keys(password)
        sleep(1.5)
        driver.find_element_by_id("submitBtn").click()
    except Exception as e:
        raise e
    finally:
        driver.close()
        driver.quit()
    end = time()
    print("Task run %0.2f seconds." % (end - start))

def list_of_groups(list_info, per_list_len):
    '''
    将列表分割成指定长度的子列表，每个列表长度为当前测试并发数
    :param list_info:   列表，需要进行参数化的总列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) *per_list_len)
    end_list = [list(i) for i in list_of_group] # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count !=0 else end_list
    return end_list

if __name__ == '__main__':
    userinfo = [
        {"username": "xiaoming", "password": "123456"},
        {"username": "dapeng", "password": "11223344"},
        {"username": "zuxiaobin", "password": "9090990"},
        {"username": "wangtao", "password": "4556677"}
    ]
    threads = []
    split_user_list = list_of_groups(userinfo,2)  # 这里只需要修改分割的数量即可实现循环登录和并发登录的数量
    print(split_user_list)
    for user_list in split_user_list:
        threads = [threading.Thread(target=user_login, args=(i["username"], i["password"])) for i in user_list]

        for t in threads:
            t.start()

        for t in threads:
            t.join()