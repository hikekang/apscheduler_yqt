#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/27 13:27
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 02.py
 Description: 使用synonyms 进行文本相似度计算
 github地址：https://github.com/chatopera/Synonyms
 Software   : PyCharm
"""
import synonyms
# print("人脸: ", synonyms.nearby("人脸"))
# print("识别: ", synonyms.nearby("识别"))
# print("NOT_EXIST: ", synonyms.nearby("NOT_EXIST"))
print("开始运行")
sen1 = "大宗商品货运，物流的下一个蓝海？ 2021年可以说是物流货运平台企业上市的大年，随着福佑、满帮和货拉拉等陆续提交上市申请，资本市场又把目光聚焦到了物流货运赛道。在这一波趋势中，可以明显发现，已提交上市的企业和有望冲击上市的企业，比如壹米滴答，主要集中在快运，壹米"
sen2 = "壹米滴答，主要集中在快运，也就是零担运输的领域，或者从运输品类上看，都以非生产型商品或消费品为主。而在中国超过6万亿的公路货运运费规模的市场中，是否还有足够的机会涌现出行业的巨头？除了非生产型商品和消费品，运输生产资料为主的大宗商品货运市场，壹米"
import time
t1=time.time()
for i in range(100):
    r = synonyms.compare(sen1, sen2, seg=True)

print(r)
print(time.time()-t1)