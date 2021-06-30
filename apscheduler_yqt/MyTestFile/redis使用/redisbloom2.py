# -*- coding: utf-8 -*-
"""
   File Name：     bloom2
   Description :
   Author :       hike
   time：          2021/4/10 16:06
"""
from redisbloom.client import Client
rb = Client()
rb.bfCreate('bloom', 0.01, 1000)
rb.bfAdd('bloom', 'foo')        # returns 1
rb.bfAdd('bloom', 'foo')        # returns 0
rb.bfExists('bloom', 'foo')     # returns 1
rb.bfExists('bloom', 'noexist') # returns 0