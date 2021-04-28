# -*- coding: utf-8 -*-
"""
   File Name：     second_data_crawl
   Description :
   Author :       hike
   time：          2021/4/27 17:25
"""
import urllib
from multiprocessing.queues import Queue
import json
from threading import Thread
import requests
from fake_useragent import UserAgent


"""
首先从TS_A库中的各个表中获取未爬取二级数据的连接
    方案一：
        或者更改表结构、重新创建一个表（id,industry_id,ic_id,keyword_id,is_crawl_data）
        查表获取信息，获取行业id，爬取数据，更新 TS_A,QBB_A,TS_B,QBB_B四个库中相对应的行业表
    方案二：
        每隔一段时间扫描表
        各个表增加字段
        查询TS_A库18个行业表，获取 id,industry_id,ic_id,keyword_id
        爬取二级数据 更新库
    方案三：
        mq发送消息队列id,industry_id,ic_id,keyword_id  实时
        爬取数据，更新 TS_A,QBB_A,TS_B,QBB_B四个库中相对应的行业表
"""

# end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# start_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
# start_time1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
# end_time1 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
# print(end_time1)
class yqtSpider(object):
    def __init__(self,data):
        self.url='http://yuqing.sina.com/newEdition/getDetail.action'
        self.headers = {
            'User-Agent': UserAgent().random,
            'Cookie': 'LOGIN_KEY=a8999383ceb1b82ad39d50164e35ad24; Hm_lvt_d535b0ca2985df3bb95f745cd80ea59e=1619321791,1619337563,1619416119,1619494308; Hm_lpvt_d535b0ca2985df3bb95f745cd80ea59e=1619494308; Hm_lvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619321791,1619337563,1619416119,1619494308; Hm_lpvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619494308; www=userSId_yqt365_hbslxx_239715_17425; JSESSIONID=4F0678BDBA81455FF183016C9BCC7ACC'
        }
        self.data=data
        # URL队列
        self.urlQueue = Queue()
        # 解析队列
        self.parseQueue = Queue()

    # URL入队列
    def getUrl(self):
        # 生成10个URL地址,放到队列中
        for da in iter(self.data):
            params = {
                'icc.id': da[2],
                'kw.keywordId': da[3]
            }
            params = urllib.parse.urlencode(params)
            # 把拼接的url放到url队列中
            fullurl = self.url + params
            self.urlQueue.put(fullurl)

    # 采集线程事件函数,发请求,把html给解析队列
    def getHtml(self):
        proxies = {'http': None, 'https': None}
        while True:
            # 如果队列不为空,则获取url
            if not self.urlQueue.empty():
                url = self.urlQueue.get()
                # 三步走
                res = requests.get(url, headers=self.headers,proxies=proxies)
                res.encoding = 'utf-8'
                html = res.text
                # data = json.loads(html)
                # 把html发到解析队列
                # self.parseQueue.put(data['icc']['content'])
                self.parseQueue.put(html)
            else:
                break

    # 解析线程事件函数,从解析队列get,提取并处理数据
    def parseHtml(self):
        while True:
            # 把html转换成json格式
            try:
                html = self.parseQueue.get(block=True, timeout=2)
                hList = json.loads(html)['data']
                # hList : [{应用信息1},{},{}]
                for h in hList:
                    # 应用名称
                    name = h['displayName']
                    # 应用链接
                    d = {
                        '应用名称': name.strip(),
                        '应用链接': 'http://app.mi.com/details?' + h['packageName']
                    }
                    with open('xiaomi.json', 'a') as f:
                        f.write(str(d) + '\n')
            except:
                break

    # 主函数
    def workOn(self):
        # url入队列
        self.getUrl()
        # 存放所有采集线程对象的列表
        tList = []
        # 存放所有解析线程对象的列表
        # 采集线程开始执行
        for i in range(5):
            t = Thread(target=self.getHtml)
            tList.append(t)
            t.start()
        # 解析线程开始执行
        for i in range(5):
            t = Thread(target=self.parseHtml)
            tList.append(t)
            t.start()
        # 统一回收解析线程
        for i in tList:
            i.join()
