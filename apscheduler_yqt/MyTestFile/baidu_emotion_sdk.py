# -*- coding: utf-8 -*-
"""
   File Name：     baidu_emotion_sdk
   Description :
   Author :       hike
   time：          2021/4/9 15:34
"""
import time
import re
APP_ID="18295264"
API_KEY="ooX8tfe05iQ8Cb1tjxY5xGx7"
SECRET_KEY="6EOG69bnEu6HsCQv0yOBO4okdrGwh3qm"
from aip import AipNlp
client=AipNlp(APP_ID,API_KEY,SECRET_KEY)

text = "招聘驾驶员、装卸工、合伙人戳这里关注我，看最新招聘信息👇公司信息:单位:海门市壹米滴答物流地址:海门市三和镇滨港大道4881号壹米滴答物流岗位一：B、C照驾驶员岗位要求："
time1=time.time()
# data=client.sentimentClassify(text)
# print(data)
# print(data['items'][0]['positive_prob'])
# time2=time.time()
# print(time2-time1)


def re_emojis(text):
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"
           u"\U0001F300-\U0001F5FF"
           u"\U0001F680-\U0001F6FF"
           u"\U0001F1E0-\U0001F1FF"
           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)
