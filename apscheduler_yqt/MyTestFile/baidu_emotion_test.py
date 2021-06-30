# -*- coding: utf-8 -*-
"""
   File Name：     baidu_emotion_test
   Description :
   Author :       hike
   time：          2021/4/9 15:16
"""
import requests
import json
my_info={
'APP_ID': "18295264",
'API_KEY':"ooX8tfe05iQ8Cb1tjxY5xGx7",
'SECRET_KEY':"6EOG69bnEu6HsCQv0yOBO4okdrGwh3qm",
}
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(my_info['API_KEY'],my_info['SECRET_KEY'])
response = requests.get(host)
access_token=''
if response:
    # print(response.json())
    access_token=response.json()['access_token']

print(access_token)


url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify&access_token=%s'%access_token
headers={
    'Content-Type':'application/json'
}
Body={
    "text": "苹果是一家伟大的公司"
}
print(url)
re=requests.post(url,headers=headers,data=Body)
print(re.json())