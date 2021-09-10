#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/6 16:47
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : clear_producer.py
 Description:
 Software   : PyCharm
"""
import pika
from utils.mylogger import logger
from utils import ssql_helper_test as ssql_helper
import re
from utils.secodnd_data_utils import crawl_second_by_requests,crawl_second_by_webdriver
web_url_selenium=re.compile('http[s]://(www.toutiao.com)|(mp.weixin.qq.com)|'
                            '(dy.163.com/v2/article/detail)|(kuaibao.qq.com)|(www.sohu.com)|(www.360kuai.com)|(view.inews.qq.com).*')
video_url=re.compile('http[s]://(v.qq.com)|(live.kuaishou.com)|(www.iesdouyin.com)|(www.ixigua.com)|(m.toutiaoimg.cn).*')
hostname='127.0.0.1'
# 1。连接
creadentails=pika.PlainCredentials('admin','admin')
connection=pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=creadentails))
clear_data_channel=connection.channel()
# 2.创建队列
clear_data_channel.queue_declare(queue="clear_data")
#3。确定回调函数
def callback_clear(_,__,___,body):
    print("清洗数据:%r"%body)
    clear_back="%r数据清洗完毕,正在进行上传"%body.decode('utf-8')
    print(clear_back)
    clear_data_channel.basic_publish(exchange='',# 简单模式
                                     routing_key='upload_data_channel',#
                                     body=body)
def quchong(dir_list, key):
    logger.info("第一次链接去重之前数据量为：%s",str(len(dir_list)))
    new_dirlist = []
    values = []
    for d in dir_list:
        if d[key] not in values:
            new_dirlist.append(d)
            values.append(d[key])


    logger.info("本次去重剩余数量为:%s", str(len(new_dirlist)))
    # 本次打开浏览器直至抓取结束的数据量
    return new_dirlist

def clear_data(_,__,___,data_list):
    """

    :param _:
    :param __:
    :param ___:
    :param data_list:
    :return:
    """
    clear_data_list=[]
    logger.info("数据处理")
    new_data_list = quchong(data_list, "链接")

    # 第二次滤重
    new_data_list = ssql_helper.filter_by_url(new_data_list, self.industry_name)
    redis_len += len(new_data_list)

    for data in new_data_list:
        # 1.标题或url为空的舍去
        if data["标题"] == "" and data["链接"] == "":
            # new_data_list.remove(data)
            continue
        #     二层正文处理
        if data["标题"] == "":
            if len(data["转发内容"]) >= 20:
                data["标题"] = data["转发内容"][0:20]
            else:
                data["标题"] = data["转发内容"]
        #2.转发微博并且转发内容为空的使舍去
        elif data["标题"] == "转发微博" and data["转发内容"] == "":
            # new_data_list.remove(data)
            print("标题为转发微博，转发内容为空")
            continue
        #3.转发类型的微博，取前内容的前20个字符作为标题
        elif data["标题"] == "转发微博":
            if len(data["转发内容"]) >= 50:
                data["标题"] = data["转发内容"][0:20]
                data['描述'] = data["转发内容"][0:120]
            else:
                data["标题"] = data["转发内容"]
                data['描述'] = data["转发内容"]

        if data['描述'] != "" and data["转发内容"] == "" and len(data["转发内容"]) == 0:
            data["转发内容"] = data['描述']

        if data['转发内容'] != "" and data['描述'] == "" and len(data['转发内容']) != 0:
            # if len(data["转发内容"]) >= 20:
            #     data["标题"] = data["转发内容"][0:20]
            # else:
            #     data['描述'] = data['转发内容']
            data['描述'] = data['转发内容']

        if data['描述']=="转发微博" and data["转发内容"] != "":
            if len(data["转发内容"]) >= 50:
                data['描述'] = data['转发内容'][0:120]
            else:
                data['描述']=data['转发内容']

        if "微博" in data['site_name']:
            # print("处理标题")
            data['标题'] =data['描述'][0:20]
            if data['sort']=='转发':
                if len(data["转发内容"]) >= 120:
                    data['描述'] = data['转发内容'][0:120]
                else:
                    data['描述'] = data['转发内容']
        if len(data['描述']) > 120:
            # print("处理描述")
            data['描述'] = data['描述'][0:120]

        if "weibo.com" in data["链接"] and data["sort"] != "":
            data['标题'] = data['描述'][0:20]
            if data["sort"] == "原创":
                data['is_original'] = 1
            elif data["sort"] == "转发":
                data['is_original'] = 0
            else:
                data['is_original'] = 2
        else:
            data['is_original'] = 2

        if "微博" not in data['site_name']:
            match_selenim=web_url_selenium.findall( data['链接'])
            if match_selenim:
                print("通过selenium抓取")
                content=crawl_second_by_webdriver(data['链接'])
                print("抓取完毕")
                if content == "":
                    data['转发内容'] += "<selenium_error hidden>" \
                                    "</selenium_error hidden>"
                if len(content)>len(data['转发内容']):
                    data['转发内容']= '<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;' \
                                  'white-space: -pre-wrap;white-space: -o-pre-wrap; ' \
                                  'word-wrap: break-word;" ><zhengwen>'+content+"</zhengwen></pre>"
                    data['转发内容']+="<selenium hidden>\n【通过selenium抓取】</selenium>"
                # self.spider_driver.switch_to.window(self.spider_driver.window_handles[0])
                # print(data['转发内容'])
            else:
                match_video=video_url.findall(data['链接'])
                if match_video:
                    print("跳过视频")
                    data['转发内容'] += "<viode_error hidden>跳过视频</viode_error hidden>"
                else:
                    content= crawl_second_by_requests(data['链接'])
                    if content=="":
                        data['转发内容']+="<requests_error hidden>requests抓取错误</requests_error hidden>"
                    if len(content) > len(data['转发内容']):
                        data['转发内容']= '<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;' \
                                  'white-space: -pre-wrap;white-space: -o-pre-wrap; ' \
                                  'word-wrap: break-word;" ><zhengwen>'+content+"</zhengwen></pre>"
                        data['转发内容'] += "<requests hidden>\n【通过request抓取】</requests>"
        clear_data_list.append(data)

#4.确定监听队列
clear_data_channel.basic_consume('clear_data',callback_clear,True)
clear_data_channel.start_consuming()