#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/18 17:03
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : post_chrome.py
 Description:
 Software   : PyCharm
"""
# 旧版
import requests
import json
data_all = 'view.keywordId=2685566&view.secondKeyword=&view.userSearchSetId=0&view.timeDomain=1' \
           '&view.startTime=2021-05-18+13%3A00%3A00&monitorType=1&view.endTime=2021-05-18+14%3A00%3A00&view.origin=1' \
           '&view.matchType=3&view.resultPresent=1&view.paixu=2&view.exportType=&view.weiboType=0&view.options=1' \
           '&view.involveWay=0&view.comblineflg=2&view.isRoot=0&page=1&pagesize=50&view.viewMode=1&kw.keywordId=2685566' \
           '&view.secondKeywordMatchType=1&view.duplicateShow=0&view.keywordProvince=%E5%85%A8%E9%83%A8' \
           '&view.duplicateShowMultiple=0&view.toolbarSwitch=0&view.bloggerAuthenticationStatus=0' \
           '&view.blogPostsStatus=0&view.ocrContentType=0&view.isRootMultiple=0&view.dataView=0' \
           '&view.bloggerAuthenticationStatusMultiple=0&view.weiboTypeMultiple=0&view.accurateSwitch=0' \
           '&view.attributeCheck=1&view.informationContentType=1'

headers_all = {
    'Accept': 'application/json,text/plain,*/*',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Content-Length': '795',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': 'JSESSIONID=7309C43EE82A37B413794875F752FFD0;www=userSId_yqt365_lsitit_850894_60500',
    'Host': 'yuqing.sina.com',
    'Origin': 'http://yuqing.sina.com',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/90.0.4430.93Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
res = requests.post(data=data_all, headers=headers_all,
                    url='http://yuqing.sina.com/newEdition/getKeywordSearchList.action')
print(res.text)
content = json.loads(res.text)
print(content['total'])

data_part = 'view.keywordId=2685566&view.secondKeyword=%E5%8D%8E%E7%A1%95&view.userSearchSetId=0&view.timeDomain=1' \
            '&view.startTime=2021-05-18+13%3A00%3A00&monitorType=1&view.endTime=2021-05-18+14%3A00%3A00&view.origin=1' \
            '&view.matchType=3&view.resultPresent=1&view.paixu=2&view.exportType=&view.weiboType=0&view.options=1' \
            '&view.involveWay=0&view.comblineflg=2&view.isRoot=0&page=1&pagesize=50&view.viewMode=1&kw.keywordId=2685566' \
            '&view.secondKeywordMatchType=1&view.duplicateShow=0&view.keywordProvince=%E5%85%A8%E9%83%A8' \
            '&view.duplicateShowMultiple=0&view.toolbarSwitch=0&view.bloggerAuthenticationStatus=0&view.blogPostsStatus=0' \
            '&view.ocrContentType=0&view.isRootMultiple=0&view.dataView=0&view.bloggerAuthenticationStatusMultiple=0' \
            '&view.weiboTypeMultiple=0&view.accurateSwitch=0&view.attributeCheck=1&view.informationContentType=1'
headers_part = {
    'Accept': 'application/json,text/plain,*/*',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': 'www=userSId_yqt365_lsitit_850894_68655;JSESSIONID=94A13F973994D5C17402F46571FFEAD5',
    'Host': 'yuqing.sina.com',
    'Origin': 'http://yuqing.sina.com',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/90.0.4430.93Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# 分词查询
res2 = requests.post(data=data_part, headers=headers_part,
                     url='http://yuqing.sina.com/newEdition/getKeywordSearchList.action')
content = json.loads(res2.text)
print(content['total'])

data_list=[]
for item in content['icclist']:
    data = {
            '时间': item['captureTime'],
            '标题': item['title'],
            '描述': item['content'],  # 微博原创
            '链接': item['webpageUrl'],
            '转发内容': item['forwarderContent'],
            '发布人': item['author'],
            'ic_id': item['id'],
            'keywords_id': item['keywordId'],  # 没有拿到
            'attitude': item['emotion'],
            'images': item['profileImageUrl'],
            'reposts_count': item['repeatNum'],
            'praiseNum':item['praiseNum'],
        # customFlagValue
            'comments_count': 0,
            'sort': item['repostsFlg'],
            'industry': item['secondTradeList'][0],
            'related_words': item['referenceKeyword'],
            'site_name': item['captureWebsiteName'],
            'area': item['province'],
                    }
