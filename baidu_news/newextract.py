# -*- coding: utf-8 -*-
"""
   File Name：     newexecute
   Description :
   Author :       hike
   time：          2021/4/19 15:28
"""
## 用Article爬取单条新闻
from newspaper import Article
# 目标新闻网址
url = 'https://www.zhihu.com/question/321865618/answer/709706336'
news = Article(url, language='zh')
news.download()        # 加载网页
# print(news.html)
news.parse()           # 解析网页
print(news.publish_date)
print('题目：',news.title)       # 新闻题目
print('正文：\n',news.text)      # 正文内容
print(news.authors)     # 新闻作者
print(news.keywords)    # 新闻关键词
print(news.summary)     # 新闻摘要


# print(news.top_image) # 配图地址
# print(news.movies)    # 视频地址
# print(news.publish_date) # 发布日期
# print(news.html)      # 网页源代码