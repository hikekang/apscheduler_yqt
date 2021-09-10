#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/12 17:19
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 03clear_data_product.py
 Description:
 Software   : PyCharm
"""
import pika
import re
from utils.mylogger import logger
# from utils import qinbaobing_ssql as ssql_helper
from utils import ssql_helper_test as ssql_helper

from yuqingtong import config
myconfig = config.redconfig()
queue_name=myconfig.getValueByDict("queue","name")
web_url_selenium=re.compile('http[s]://(www.toutiao.com)|(mp.weixin.qq.com)|'
                            '(dy.163.com/v2/article/detail)|(kuaibao.qq.com)'
                            '|(www.sohu.com)|(www.360kuai.com)|(view.inews.qq.com)|'
                            '(tousu.sina.com.cn)|(www.chasfz.com)|(mbd.baidu.com)|'
                            '(wap.peopleapp.com)|(www.xiaohongshu.com)|'
                            '(www.laihema.com)|(kuaibao.qq.com).*')
video_url=re.compile('http[s]://(v.qq.com)|(live.kuaishou.com)'
                     '|(www.iesdouyin.com)|(www.ixigua.com)|(m.toutiaoimg.cn)|'
                     '(www.dongchedi.com)|(kandianshare.html5.qq.com/v2/video)|'
                     '(www.dttt.net)|(www.zgwgfw.com).*')

credentials=pika.PlainCredentials('qb_03','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1',port=5672,virtual_host='/',credentials=credentials,heartbeat=0))
channel = connection.channel()

channel.queue_declare(queue=f'{queue_name}_clear_data',durable=True)
channel.queue_declare(queue=f'{queue_name}_upload_data',durable=True)
# 第一次根据爬取链接去重
def quchong(dir_list, key):
    logger.info("第一次链接去重之前数据量为：%s"%str(len(dir_list)))
    new_dirlist = []
    values = []
    for d in dir_list:
        if d[key] not in values:
            new_dirlist.append(d)
            values.append(d[key])
    return new_dirlist
def spider_clear_data(data_list,clear_data_list,info):
    logger.info("数据处理")
    new_data_list = quchong(data_list, "链接")
    # title_pattern = re.compile('<zhengwen>([\s\S.]*)</zhengwen>')
    # 第二次滤重
    new_data_list = ssql_helper.filter_by_url(new_data_list, info['industry_name'])
    for data in new_data_list:
        # content = title_pattern.findall(data["转发内容"])[0]
        content=data['转发内容']
        # 1.标题或url为空的舍去
        if data["标题"] == "" and data["链接"] == "":
            # new_data_list.remove(data)
            continue
        #     二层正文处理
        if data["标题"] == "":
            if len(content) >= 20:
                data["标题"] = content[0:20]
            else:
                data["标题"] = content
        # 2.转发微博并且转发内容为空的舍去
        elif data["标题"] == "转发微博" and data["转发内容"] == "":
            # new_data_list.remove(data)
            logger.info("标题为转发微博，转发内容为空")
            continue
        # 3.转发类型的微博，取前内容的前20个字符作为标题
        elif "转发微博" in data["标题"]  :
            if len(content) >= 50:
                data["标题"] = content[0:20]
                data['描述'] = content[0:120]
            else:
                data["标题"] = content
                data['描述'] = content

        if data['描述'] != "" and content == "" and len(content) == 0:
            data["转发内容"] = data['描述']

        if data['转发内容'] != "" and data['描述'] == "" and len(content) != 0:
            data['描述'] = content

        if  "转发微博" in data['描述'] and content != "":
            if len(content) >= 50:
                data['描述'] = content[0:120]
            else:
                data['描述'] = content

        if "微博" in data['site_name']:
            # print("处理标题")
            data['标题'] = data['描述'][0:20]
            if data['sort'] == '转发':
                if len(content) >= 120:
                    data['描述'] = content[0:120]
                else:
                    data['描述'] = content
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
        data['标题'] = data['标题'][0:50]
        data['标题']=re.sub('\s+','',data['标题'])
        data['描述']=re.sub('\s+','',data['描述'])
        data['转发内容']=re.sub('\s+','',data['转发内容'])
        clear_data_list.append(data)

def clear_data(ch, method, properties, body):
    """
    解析数据
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    dict_body = eval(body.decode('utf-8'))
    # print(dict_body)
    #将源码传入抓取队列，进行抓取
    print("进行抓取解析")
    clear_data_list=[]
    spider_clear_data(dict_body['data'],clear_data_list,dict_body['info'])
    print("抓取完毕进行上传")
    if clear_data_list:
        upload_data = {
        'data': clear_data_list,
        'info': dict_body['info'],
        'datacenter_id': dict_body['datacenter_id']
        }
        channel.basic_publish(exchange='',
                              routing_key=f'{queue_name}_upload_data',
                              body=str(upload_data))
    # 手动应答，效率会降低
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=f'{queue_name}_clear_data',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=clear_data)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()