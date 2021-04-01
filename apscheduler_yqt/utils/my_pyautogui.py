# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 23:02
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : my_pyautogui.py


import pyautogui as pyautogui
import time

# pyautogui.PAUSE = 1  # 调用在执行动作后暂停的秒数，只能在执行一些pyautogui动作后才能使用，建议用time.sleep
pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常

