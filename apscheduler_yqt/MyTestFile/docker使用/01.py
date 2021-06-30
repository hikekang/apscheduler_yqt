#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/15 13:39
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from flask import Flask

app=Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello,Docker'


