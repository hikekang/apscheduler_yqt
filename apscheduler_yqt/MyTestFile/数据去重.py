# -*- coding: utf-8 -*-
"""
   File Name：     数据去重
   Description :
   Author :       hike
   time：          2021/4/7 16:35
"""
from functools import reduce

dir_list=[
    {
        "name": "hike",
        "age": "18"
    },
    {
        "name": "hike2",
        "age": "19"
    },
    {
        "name": "hike3",
        "age": "9"
    },
    {
        "name": "hike1",
        "age": "18"
    },
]
# print(list(set(dir_list)))

values=[]
new_data=[]
for d in dir_list:
    if d["age"] not in values:
        new_data.append(d)
        values.append(d['age'])


print(new_data)

def deleteDuplicate(li):
    func = lambda x, y: x if y in x else x + [y]
    li = reduce(func, [[], ] + li)
    return li

def deleteDuplicate(li):
    temp_list = list(set([str(i) for i in li]))
    li=[eval(i) for i in temp_list]
    return li
print(deleteDuplicate(new_data))


def quchong(dir_list, key):
    new_dirlist = []
    values = []
    for d in dir_list:
        if d[key] not in values:
            new_dirlist.append(d)
            values.append(d[key])
    return new_dirlist
print(quchong(new_data,"age"))

for d in new_data:
    new_data.remove(d)
    print(new_data)
config = {
        'server': '223.223.180.9',
        'user': 'tuser1',
        'password': 'tsuser1@123aA',
        'database': 'TS_B2.0',
        'port': '39999'
    }
def get_industry_name(*args):
    print(args)
get_industry_name(config)