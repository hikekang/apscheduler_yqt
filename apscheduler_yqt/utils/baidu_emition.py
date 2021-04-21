# -*- coding: utf-8 -*-
"""
   File Name：     baidu_emition
   Description :
   Author :       hike
   time：          2021/4/10 10:55
"""
from aip import AipNlp
import re
import time
APP_ID="18295264"
API_KEY="ooX8tfe05iQ8Cb1tjxY5xGx7"
SECRET_KEY="6EOG69bnEu6HsCQv0yOBO4okdrGwh3qm"

def emotion(text):
    client=AipNlp(APP_ID,API_KEY,SECRET_KEY)
    data=client.sentimentClassify(re_emojis(text))
    print(data)
    if 'error_msg' in data.keys():
        time.sleep(2)
        return emotion(text)
    else:
        return data['items'][0]['positive_prob']

def re_emojis(text):
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"
           u"\U0001F300-\U0001F5FF"
           u"\U0001F680-\U0001F6FF"
           u"\U0001F1E0-\U0001F1FF"
           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)