#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/17 16:37
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : post2.py
# @Software: PyCharm
# multipart/form-data

"""
通过接口获取数据 只需要keywordid，cookie,start_time,end_time
    多项目运行，速度快
缺点有个别乱码

"""
import json

import requests
class MultipartFormData(object):
    """multipart/form-data格式转化"""

    @staticmethod
    def format(data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW", headers={}):
        """
        form data
        :param: data:  {"req":{"cno":"18990876","flag":"Y"}}
        :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
        :return: str
        :rtype: str
        """
        # 从headers中提取boundary信息
        if "content-type" in headers:
            fd_val = str(headers["content-type"])
            if "boundary" in fd_val:
                fd_val = fd_val.split(";")[1].strip()
                boundary = fd_val.split("=")[1].strip()
            else:
                raise Exception("multipart/form-data头信息错误，请检查content-type key是否包含boundary")
        # form-data格式定式
        jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
        end_str = "--{}--".format(boundary)
        args_str = ""

        if not isinstance(data, dict):
            raise Exception("multipart/form-data参数错误，data参数应为dict类型")
        for key, value in data.items():
            args_str = args_str + jion_str.format(boundary, key, value)

        args_str = args_str + end_str.format(boundary)
        args_str = args_str.replace("\'", "\"")
        return args_str


headers = {
    'content-type': "multipart/form-data; boundary=-----------------------------206056234836319224712871584608",
    'Host': 'yuqing.sina.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Authorization': 'Bearer',
    'Origin': 'http://yuqing.sina.com',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=7309C43EE82A37B413794875F752FFD0;www=userSId_yqt365_lsitit_850894_60500',
}

data = {
    "searchCondition": {"keywordId": 2685566, "accurateSwitch": 1, "bloggerAuthenticationStatusMultiple": "0",
                        "blogPostsStatus": 0, "comblineflg": 2, "dataView": 0, "displayIcon": 1, "involveWay": 0,
                        "keywordProvince": "全部", "matchType": 3, "ocrContentType": 0, "searchRootWbMultiple": "0",
                        "searchType": "null", "timeDomain": "1", "weiboTypeMultiple": "0", "firstOrigin": "null",
                        "sencondOrigin": "null", "secondKeywordMatchType": 1, "searchSecondKeyword": "",
                        "webSiteId": "0", "order": 2, "monitorType": 1, "isRoot": 1, "origins": "1",
                        "presentResult": "1", "options": "1", "attributeCheck": "1", "informationContentType": 1,
                        "duplicateShowMultiple": "0", "attribute": "1", "chartStart": "2021-05-17 00:00:00",
                        "chartEnd": "2021-05-17 23:59:59", "page": 50, "pageSize": 100}
}
d2 = {"searchCondition": {
    "keywordId": 2685566,
    "accurateSwitch": 1,
    "bloggerAuthenticationStatusMultiple": "0",
    "blogPostsStatus": 0,
    "comblineflg": 2,
    "dataView": 0,
    "displayIcon": 1,
    "involveWay": 0,
    "keywordProvince": "全部",
    "matchType": 3,
    "ocrContentType": 0,
    "searchRootWbMultiple": "0",
    "timeDomain": "-1",
    "weiboTypeMultiple": "0",
    "secondKeywordMatchType": 1,
    "searchSecondKeyword": "",
    "webSiteId": "0",
    "order": 2,
    "monitorType": 1,
    "isRoot": 1,
    "origins": "1",
    "presentResult": "1",
    "options": "1",
    "attributeCheck": "1",
    "informationContentType": 1,
    "duplicateShowMultiple": "0",
    "startTime": "2021-05-17 00:00:00",
    "endTime": "2021-05-17 23:59:59",
    "attribute": "1",
    "chartStart": "2021-05-17 00:00:00",
    "chartEnd": "2021-05-17 23:59:59",
    "page": 1,
    "pageSize": 25
}}
d3 = {"searchCondition": {"keywordId": 2685566, "accurateSwitch": 1, "bloggerAuthenticationStatusMultiple": "0",
                          "blogPostsStatus": 0, "comblineflg": 2, "dataView": 0, "displayIcon": 1, "involveWay": 0,
                          "keywordProvince": "全部", "matchType": 3, "ocrContentType": 0, "searchRootWbMultiple": "0",
                          "searchType": None, "timeDomain": "1", "weiboTypeMultiple": "0", "firstOrigin": None,
                          "sencondOrigin": None, "secondKeywordMatchType": 1, "searchSecondKeyword": "",
                          "webSiteId": "0", "order": 2, "monitorType": 1, "isRoot": 1, "origins": "1",
                          "presentResult": "1", "options": "1", "attributeCheck": "1", "informationContentType": 1,
                          "duplicateShowMultiple": "0", "attribute": "1", "chartStart": "2021-05-19 00:00:00",
                          "chartEnd": "2021-05-19 23:59:59", "page": 2, "pageSize": 50}}
if __name__ == '__main__':

    # mh = MultipartFormData.format(data=data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW")
    mh = MultipartFormData.format(data=d2, headers=headers)
    # print(mh)


    res = requests.request("POST", data=mh.encode('utf-8'), headers=headers,
                           url='http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList')
    # print(res.text)

    content = json.loads(res.text)
    # print(content)
    print(type(content['data']['icontentCommonNetList']))
    for i, item in enumerate(content['data']['icontentCommonNetList']):
        print(i)
        # 作者
        author = item.get('author')
        # print(author)
        # 抓取站点名字
        captureWebsiteName = item['captureWebsiteName']
        # 城市
        city = item['city']
        # 评论数量
        comments = item['comments']
        # 内容  二次数据
        content = item['content']
        # print(content)
        # print("__________" * 20)
        # 域名
        domain = item['domain']
        # 情感
        emotion = item['emotion']
        # 转发内容
        forwarderContent = item['forwarderContent']

        id = item['id']
        keywordId = item['keywordId']
        # 个人资料图片网址
        profileImageUrl = item['profileImageUrl']
        # 城市
        province = item['province']
        # 发布时间
        publishedMinute = item['publishedMinute']
        # 关键词
        referenceKeyword = item['referenceKeyword']
        # 是否转发 1为转发  0为原创
        repostsFlg = item['repostsFlg']
        # 行业  是一个列表
        secondTradeList = item['secondTradeList']
        # 简介 非微博
        summary = item['summary']
        # 标题  带有：
        title = item['title']
        # 原文链接
        webpageUrl = item['webpageUrl']
        # 微博转发url
        forwarderImages = item['forwarderImages']
        # 转发数量
        forwardNumber = item['forwardNumber']

        # 微博链接
        rootWeiboUrl = item['rootWeiboUrl']
        # 原文链接
        webpageUrl = item['webpageUrl']
        # print(webpageUrl)

    # for 循环请求 设置时间，每次selenium修改关键词后拿一次cookie
