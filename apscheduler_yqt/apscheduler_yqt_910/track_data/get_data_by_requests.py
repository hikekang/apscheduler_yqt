# _*_coding:utf-8 _*_
# @Time　　:2021/9/16   13:36
# @Author　 : Ben
# @ File　　  :get_data_by_requests.py
# @Software  :PyCharm
# @Description  通过requests请求抓取微博详细动态的 评论 转发 点赞数
import re

import requests
from lxml import etree
import traceback
from fake_useragent import UserAgent
weibo_ur='https://weibo.com/7613603858/Kh4OSe7vt?type=comment'
headers={
    # 'User-Agent': UserAgent().random,
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",

}
def get_data_item(weibourl):
    # 登录的cookie
    # weibo_cookies={
    #     'SINAGLOBAL':'5286082600493.915.1631081674384',
    #     'UOR':',,www.baidu.com',
    #     '_s_tentry':'-',
    #     'Apache':'8905968686058.805.1631755756289',
    #     'ULV':'1631755756300:5:5:2:8905968686058.805.1631755756289:1631672448972',
    #     'SUB':'_2A25MRt-cDeRhGeFL4lMY-CjFyjmIHXVvNbZUrDV8PUNbmtANLVnTkW9NfZ0FJAiAytQ6WcVoCnmYPav4y45h-B_Z',
    #     'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WhLJAV51C0zvoh9qfWali7K5JpX5KzhUgL.FoMf1K241hq4eK-2dJLoI7_QIg_LIs8D9svV97tt',
    #     'ALF':'1663296332',
    #     'SSOLoginState':'1631760332',
    #     'wb_view_log_7591986915':'1920*10801%261920*10802',
    #     "webim_unReadCount":"%7B%22time%22%3A1631761576334%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A16%2C%22msgbox%22%3A0%7D"
    # }


    weibo_cookies={
        'SINAGLOBAL':'5286082600493.915.1631081674384',
        '_s_tentry':'-',
        'Apache':'8905968686058.805.1631755756289',
        'ULV':'1631755756300:5:5:2:8905968686058.805.1631755756289:1631672448972',
        'WBtopGlobal_register_version':'2021091610',
        'wb_view_log_7591986915':'1920*10801',
        # 'webim_unReadCount':'%7B%22time%22%3A1631762431264%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A16%2C%22msgbox%22%3A0%7D',
        'SUB':'_2AkMWHjc-dcPxrARUkfkcxG3rbYhH-jyly17IAn7uJhMyAxh77k8WqSVutBF-XASOjF-MNKW7IwWK7NiUxJe9-D3s',
        'SUBP':'0033WrSXqPxfM72wWs9jqgMF55529P9D9WhLJAV51C0zvoh9qfWali7K5JpVF02feKMfeK5peoe4',
        'login_sid_t':'26d29cd705a0d5ec21d19e1562a3ad90',
        'cross_origin_proto':'SSL',
        'WBStorage':'d335429e|undefined',
        'UOR':',,login.sina.com.cn',
        'wb_view_log':'1920*10801',
    }
    proxy={
        "http":None,
        "https":None,
    }

    result=requests.get(url=weibourl,cookies=weibo_cookies,proxies=proxy)
    match=re.findall("<script>FM.view(.*)</script>",result.text)
    try:
        html_content=eval(match[-1])['html'].replace('\\','')
        doc=etree.HTML(html_content)
        li_list=doc.xpath('//ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li')
        zhuanfa=li_list[1].xpath('.//span[@class="line S_line1"]/span/em')[-1].text
        pinglun=li_list[2].xpath('.//span[@class="line S_line1"]/span/em')[-1].text
        dianzan=li_list[3].xpath('.//span[@class="line S_line1"]/span/em')[-1].text
        if zhuanfa == "转发":
            zhuanfa = '0'
        if pinglun == "评论":
            pinglun = '0'
        if dianzan == "赞":
            dianzan = '0'
        print(zhuanfa, dianzan, pinglun)
        return int(zhuanfa), int(pinglun), int(dianzan)
    except Exception as e:
        print(traceback.format_exc())
        return 0,0,0
if __name__ == '__main__':
    get_data_item("None")