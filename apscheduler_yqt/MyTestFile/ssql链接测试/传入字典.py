# -*- coding: utf-8 -*-
"""
   File Name：     传入字典
   Description :
   Author :       hike
   time：          2021/5/7 10:32
"""
class hike:
    def __init__(self,name,age):
        print(name,age)



info={
    "name":"hike",
    "age":18
}

person=hike(**info)