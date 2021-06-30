#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/18 13:30
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : post_helper.py
# @Software: PyCharm
"""

发包拿到数据

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



# 头部
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
    'Cookie': 'www=userSId_yqt365_lsitit_850894_55983;JSESSIONID=B4A58ABCD5C99A4B267C7E8B32A2DD32; ',
}
# 查询全部
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
    "searchSecondKeyword": "",  # 分词进行抓取
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
    "startTime": "2021-05-18 00:00:00",
    "endTime": "2021-05-18 23:59:59",
    "attribute": "1",
    "chartStart": "2021-05-18 00:00:00",
    "chartEnd": "2021-05-18 23:59:59",
    "page": 5,
    "pageSize": 25
}}

# 分词
d3 = {"searchCondition": {"keywordId": 2720405, "accurateSwitch": 1, "bloggerAuthenticationStatusMultiple": "0",
                          "blogPostsStatus": 0, "comblineflg": 2, "dataView": 0, "displayIcon": 1, "involveWay": 0,
                          "keywordProvince": "全部", "matchType": 3, "ocrContentType": 0, "searchRootWbMultiple": "0",
                          "searchType": '', "timeDomain": "1", "weiboTypeMultiple": "0", "firstOrigin": '',
                          "sencondOrigin": '', "secondKeywordMatchType": 1, "searchSecondKeyword": "google|联想|华硕|华为",
                          "webSiteId": "0", "order": 2, "monitorType": 1, "isRoot": 1, "origins": "1",
                          "presentResult": "1", "options": "1", "attributeCheck": "1", "informationContentType": 1,
                          "duplicateShowMultiple": "0", "attribute": "1", "chartStart": "2021-06-24 12:59:59",
                          "chartEnd": "2021-06-24 13:59:59", "page": 1, "pageSize": 100}}
d4={
'view.keywordId':'2720405',
'view.secondKeyword':'',
'view.userSearchSetId':'749212',
'view.timeDomain':'24',
'view.startTime':'',
'monitorType':'1',
'view.endTime':'',
'view.origin':'1',
'view.matchType':'3',
'view.resultPresent':'1',
'view.paixu':'2',
'view.exportType':'',
'view.weiboType':'0',
'view.options':'1',
'view.involveWay':'0',
'view.comblineflg':'2',
'view.isRoot':'0',
'page':'1',
'pagesize':'50',
'view.viewMode':'1',
'kw.keywordId':'2720405',
'view.secondKeywordMatchType':'1',
'view.duplicateShow':'0',
'view.keywordProvince':'全部',
'view.duplicateShowMultiple':'0',
'view.toolbarSwitch':'0',
'view.bloggerAuthenticationStatus':'0',
'view.blogPostsStatus':'0',
'view.ocrContentType':'0',
'view.isRootMultiple':'0',
'view.dataView':'0',
'view.bloggerAuthenticationStatusMultiple':'0',
'view.weiboTypeMultiple':'0',
'view.accurateSwitch':'1',
'view.attributeCheck':'1',
'view.informationContentType':'1',
}

class SecondData():
    def __init__(self, cookie, payload):
        self.cookie = cookie
        self.payload = payload
        pass

    # 新版
    # http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList

    # 旧版
    # http://yuqing.sina.com/newEdition/getKeywordSearchList.action

    # 正常使用
    # http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList

    # 新接口
    # 2021-06-17 18:14:04
    def get_content(self):
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
            'Cookie': self.cookie,
        }
        mh = MultipartFormData.format(data=self.payload, headers=headers)
        res = requests.request("POST", data=mh.encode('utf-8'), headers=headers,
                               url='http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList')
        content = json.loads(res.text)
        if content['data']:
            return content
        else:
            return None

    def get_content_by_keywords_2(self):
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
            'Cookie': self.cookie,
        }
        mh = MultipartFormData.format(data=self.payload, headers=headers)
        res = requests.request("POST", data=mh.encode('utf-8'), headers=headers,
                               url='http://yuqing.sina.com/newEdition/getKeywordSearchList.action')
        # print(res.text)
        content = json.loads(res.text)
        # print(content)
        if content['data']:
            return content
        else:
            return None

    def get_content_by_keywords(self):
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
            'Cookie': self.cookie,
        }
        mh = MultipartFormData.format(data=self.payload, headers=headers)
        res = requests.request("POST", data=mh.encode('utf-8'), headers=headers,
                               url='http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList')
        # print(res.text)
        content = json.loads(res.text)
        # print(content)
        if content['data']:
            return content
        else:
            return None
if __name__ == '__main__':
    # mh = MultipartFormData.format(data=data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW")
    mh = MultipartFormData.format(data=d3, headers=headers)
    print(mh)
    # print(mh)
    se=SecondData('www=userSId_yqt365_lsyousu_827857_40091;WS_KEY=79791d0d71403fbab7fafe2f60cf7747;JSESSIONID=3DB6F1761877CC7027A21BE112DCEE69;',d3)

    # print(se.get_content())
    keywords_content=se.get_content_by_keywords()
    print("hike")
    # res = requests.request("POST", data=mh.encode('utf-8'), headers=headers,
    #                        url='http://yuqing.sina.com/gateway/monitor/api/data/search/auth/keyword/getSearchList')
    # print(res.text)
    # #
    # content = json.loads(res.text)
    # print(content)
    # print(type(content['data']))
    # # 总数
    # print(content['data']['totalCount'])
    # print(content['data']['maxpage'])
    # print(type(content['data']))

    # for item in content['data']['icontentCommonNetList']:
    #     # 作者
    #     author = item.get('author')
    #     # 抓取站点名字
    #     captureWebsiteName = item['captureWebsiteName']
    #     # 城市
    #     city = item['city']
    #     # 评论数量
    #     comments = item['comments']
    #     # 内容  二次数据
    #     content = item['content']
    #     # 域名
    #     domain = item['domain']
    #     # 情感
    #     emotion = item['emotion']
    #     # 转发内容
    #     forwarderContent = item['forwarderContent']
    #
    #     id = item['id']
    #     keywordId = item['keywordId']
    #     # 个人资料图片网址
    #     profileImageUrl = item['profileImageUrl']
    #     # 城市
    #     province = item['province']
    #     # 发布时间
    #     publishedMinute = item['publishedMinute']
    #     # 关键词
    #     referenceKeyword = item['referenceKeyword']
    #     # 是否转发 1为转发  0为原创
    #     repostsFlg = item['repostsFlg']
    #     # 行业  是一个列表
    #     secondTradeList = item['secondTradeList']
    #     # 简介 非微博
    #     summary = item['summary']
    #     # 标题  带有：
    #     title = item['title']
    #     # 原文链接
    #     webpageUrl = item['webpageUrl']
    #     # 微博转发url
    #     forwarderImages = item['forwarderImages']
    #     # 转发数量
    #     forwardNumber = item['forwardNumber']
    #
    #     # 微博链接
    #     rootWeiboUrl = item['rootWeiboUrl']
    #     # 原文链接
    #     webpageUrl = item['webpageUrl']
    #     print(webpageUrl)
