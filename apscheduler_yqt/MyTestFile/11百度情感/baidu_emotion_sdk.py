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

text = "15309347317 ➤旺铺转让 【A001】我公司负责镇原县安能物流（全境），各项手续齐全。现月均到货量30吨--50吨，有稳定的客户资源，企业客户利润空间大，盈利可观。接手即可运转盈利。因其他原因，一个人经营管理太累，现对外一次性转让。"
time1=time.time()
# data=client.sentimentClassify(text)
# print(data)
# print(data['items'][0]['positive_prob'])
# time2=time.time()
# print(time2-time1)

print(client.sentimentClassify(text))
def re_emojis(text):
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"
           u"\U0001F300-\U0001F5FF"
           u"\U0001F680-\U0001F6FF"
           u"\U0001F1E0-\U0001F1FF"
           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)
