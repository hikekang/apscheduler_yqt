#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/17 15:02
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01数据解析.py
 Description:
 Software   : PyCharm
"""

import json
from utils.extract_content import extract_content as ex
st="hike"

with open("data.json","r+",encoding="utf-8") as file:
    data=file.read()
    data=data.replace("true","True").replace("false","False")
data_dict=eval(data)
print(data_dict['flag'])
data_list=[]
import re
for item in data_dict['data']['icontentCommonNetList']:
    data = {
        # '时间': item['captureTime'].replace("T"," ").replace(".000+0000",""),
        '时间': item['publishedMinute'],
        '标题': (item['title']) if item['title'] != None else item['title'],
        '描述': (item['summary']) if item['summary'] != None else item['summary'],  # 微博原创
        '链接': item['webpageUrl'],
        '转发内容': '',
        '发布人': item.get('author'),
        'ic_id': item['id'],
        'keywords_id': item['keywordId'],
        # attitude:item['distrution']
        'attitude': item['emotion'],
        'images': "",
        # 'reposts_count': item['forwardNumber'],
        'comments_count': 0,
        'sort': '转发' if int(item['repostsFlg']) == 1 else '原创',
        'industry': ",".join(item['secondTradeList']),
        'related_words': item['referenceKeyword'],
        'site_name': item['captureWebsiteName'],
        # 'area': item['contentAddress'],
        'area': item['province'],
        # 'C_Id': self.info['id']  # 客户id
    }

    if item['content'] != None:
        data['转发内容'] += ex(item['content'])
        # print(data['转发内容'])
        # print('content')
    if 'forwarderContent' in item.keys():
        if item['forwarderContent'] != None:
            data['转发内容'] += ex(item['forwarderContent'])
        # print('forwarderContent')

    if 'ocrContents' in item.keys():
        if item['ocrContents'] != None:
            data['转发内容'] += ex(item['ocrContents'])
            # print('ocrContents')

    # if item['forwarderImages']:
    #     for item_pic in item['forwarderImages']:
    #         data['images']+=item_pic['bmiddlePic']
    # if data['sort'] == '原创':
    #     data['转发内容'] = data['描述']

    # if len(data['标题']) > 20:
    #     data['标题'] = data['标题'][0:20]
    if data['发布人']:
        if '：' in data['发布人'] or ":" in data['发布人']:
            publish_man = re.sub(':|：', '', data['发布人'])
            # publish_man=data['发布人'].split(":")[0]
            data['发布人'] = publish_man
        else:
            if (len(data['发布人']) > 10):
                data['发布人'] = ''
        if (len(data['发布人']) > 15):
            data['发布人'] = ''
    if item['customFlag1'] == '5':
        data['positive_prob_number'] = 0.65
    # 非敏感
    elif item['customFlag1'] == '4':
        data['positive_prob_number'] = 0.9
    # 敏感
    elif item['customFlag1'] == '2':
        data['positive_prob_number'] = 0.1
    else:
        data['positive_prob_number'] = 0.9

    # if data['attitude'] == '中性':
    #     data['positive_prob_number'] = 0.5
    # elif data['attitude'] == '喜悦':
    #     data['positive_prob_number'] = 0.1
    # else:
    #     data['positive_prob_number'] = 0.9
    data_list.append(data)
print(data_list)
