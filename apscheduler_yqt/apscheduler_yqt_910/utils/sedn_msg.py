#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/25 13:38
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : sedn_msg.py
 Description:
 Software   : PyCharm
"""
import requests
#https://open.feishu.cn/open-apis/bot/v2/hook/1da2c966-e497-4938-8b77-b2b9b49d50af
def send_feishu_msg(text, hook_token="1da2c966-e497-4938-8b77-b2b9b49d50af"):
    """
    使用飞书发送消息
    :param text:发送消息的文本
    :param hook_token:
    :return:
    """
    if not hook_token:
        feishu_url_list = [""]
    else:
        feishu_url_list = ["https://open.feishu.cn/open-apis/bot/v2/hook/" + hook_token]
    for feishu_url in feishu_url_list:
        res = requests.post(feishu_url, json={
            "msg_type": "text",
            "content": {
                "text": text
            }
        }, verify=False,proxies={
            "http":None,
            "https":None
        })
        # Utils.getLogger().info("send_feishu_msg req : {} , res:{}".format(text, res.text))
        try:
            if res.json()["StatusCode"] == 0:
                break
        except:
            print(f"飞书--{res}")