#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/2 17:05
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : qinggan.py
 Description:
 Software   : PyCharm
"""
import json
str='{"正面":0.0,"中性":0.0,"非敏感":1.0,"敏感":0.0}'

emotion_dict=json.loads(str)
result=max(emotion_dict,key=emotion_dict.get)
print(result)
