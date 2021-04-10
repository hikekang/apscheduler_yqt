# -*- coding: utf-8 -*-
"""
   File Name：     baidu_emition
   Description :
   Author :       hike
   time：          2021/4/10 10:55
"""
from aip import AipNlp


APP_ID="18295264"
API_KEY="ooX8tfe05iQ8Cb1tjxY5xGx7"
SECRET_KEY="6EOG69bnEu6HsCQv0yOBO4okdrGwh3qm"

def emotion(text):
    client=AipNlp(APP_ID,API_KEY,SECRET_KEY)
    data=client.sentimentClassify(text)
    return data['items'][0]['positive_prob']
