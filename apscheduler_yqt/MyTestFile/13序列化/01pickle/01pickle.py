#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/13 10:07
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01pickle.py
 Description:
 Software   : PyCharm
"""
import pickle

if __name__ == '__main__':

    var_a={
        'name':"HIKE",
        'AGE':'18'
    }
    var_b=pickle.dumps(var_a)
    print(var_b)
    var_c=pickle.loads(var_b)
    print(var_c)

    with open ("test.text","wb") as f:
        pickle.dump(var_a,f)

    with open("test.text","rb") as f:
        var_load=pickle.load(f)
    print(var_load)