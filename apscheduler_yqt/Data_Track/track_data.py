# -*- coding: utf-8 -*-
"""
   File Name：     track_data
   Description :
   Author :       hike
   time：          2021/4/15 9:56
"""
from utils.ssql_helper import get_teack_datas
from fake_useragent import UserAgent
url_list=get_teack_datas()
header={
    "User_Agent":UserAgent().random,
    "Cookie":'login_sid_t=41e255698cb00e41abf368eb45f0af82; cross_origin_proto=SSL; WBStorage=8daec78e6a891122|undefined; _s_tentry=www.google.com.hk; UOR=www.google.com.hk,weibo.com,www.google.com.hk; Apache=281520003102.6044.1618457244484; SINAGLOBAL=281520003102.6044.1618457244484; ULV=1618457244491:1:1:1:281520003102.6044.1618457244484:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhLJAV51C0zvoh9qfWali7K5JpX5o275NHD95QNSK.p1Knc1K2fWs4DqcjTIsLu9gyyIgxadJMt; SSOLoginState=1618457263; SUB=_2A25Nc8LiDeRhGeFL4lMY-CjFyjmIHXVuCLMqrDV8PUNbmtANLU73kW9NfZ0FJCTqlNv6-S7fXTS0B1U9wRvyqLL5; ALF=1649993263; wvr=6; wb_view_log_7591986915=1920*10801; webim_unReadCount=%7B%22time%22%3A1618457423716%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A3%2C%22msgbox%22%3A0%7D'
}

# curl -i http://api.t.sina.com.cn/queryid.json?mid=K9wsJF0lz=1&type=2
print(url_list)
# proxies={"http":None,"https":None}
#
# url='https://www.weibo.com/aj/v6/comment/big?ajwvr=6&id=4622697419772785&from=singleWeiBo&__rnd=1618470131775' #转发
# # https://www.weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4622697419772785&__rnd=1618471027884  评论
# r=requests.get(url,headers=header,proxies=proxies)
# # print(r.text)
# # html=etree.HTML(r.text)
# html=r.content.decode('utf-8','ignore')
# print(type(html))
# j=json.loads(html)
# print(type(j))
# print(j['data']['count'])
# # print(j['data']['html'])
# # print(url_list)
