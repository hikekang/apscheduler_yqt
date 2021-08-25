#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/25 11:57
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:使用飞书发送消息
 Software   : PyCharm
"""
import requests
#https://open.feishu.cn/open-apis/bot/v2/hook/1da2c966-e497-4938-8b77-b2b9b49d50af
def send_feishu_msg(text, hook_token="1da2c966-e497-4938-8b77-b2b9b49d50af"):
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
        }, verify=False)
        # Utils.getLogger().info("send_feishu_msg req : {} , res:{}".format(text, res.text))
        try:
            if res.json()["StatusCode"] == 0:
                print(res.json())
                break
        except:
            print(f"飞书--{res}")

if __name__ == '__main__':
    send_feishu_msg("这个是测试")