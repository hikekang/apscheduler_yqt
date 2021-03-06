# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/5/8 10:48
"""
# _*_coding:utf_8_
import BitVector
import os
import sys


class SimpleHash():

    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            # 加权求和
            ret += self.seed * ret + ord(value[i])
        # 位运算保证最后的值在0到self.cap之间
        return (self.cap - 1) & ret


class BloomFilter():

    def __init__(self, BIT_SIZE=1 << 25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []

        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))
        print(self.hashFunc)

    def insert(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1
        print(self.bitset)

    def is_contaions(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            ret = ret & self.bitset[loc]
        return ret
