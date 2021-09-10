#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/12 17:18
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 02spider_xpath_product.py
 Description:
 Software   : PyCharm
"""
import pika
from utils.mylogger import logger
from utils.extract_content import extract_content as ex
from yuqingtong import config
myconfig = config.redconfig()
queue_name=myconfig.getValueByDict("queue","name")
credentials = pika.PlainCredentials('qb_02', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='/', credentials=credentials,heartbeat=0))
channel = connection.channel()
channel.queue_declare(queue=f'{queue_name}_xpath', durable=True)
channel.queue_declare(queue=f'{queue_name}_clear_data', durable=True)


def _parse(page_source, info_id):
    data_list=[]
    for item in page_source['data']['icontentCommonNetList']:
        data = {
            '时间': item['publishedMinute'],
            '标题': ex(item['title']) if item['title'] != None else item['title'],
            '描述': ex(item['summary']) if item['summary'] != None else item['summary'],  # 微博原创
            '链接': item['webpageUrl'],
            '转发内容': '',
            '发布人': item.get('author'),
            'comments_count': 0,
            'sort': '转发' if int(item['repostsFlg']) == 1 else '原创',
            'related_words': item['referenceKeyword'],
            'site_name': item['captureWebsiteName'],
            'area': item['province'],
            'C_Id': info_id  # 客户id
        }
        # 标题处理冒号规则
        r1 = data['标题'].split(":")
        r2 = data['标题'].split("：")
        if len(r1) > 1:
            data['标题'] = ''.join(r1[1:])
        elif len(r2) >1:
            data['标题'] = ''.join(r2[1:])
        if item['content'] != None:
            data['转发内容'] += item['content']

        if 'forwarderContent' in item.keys():
            if item['forwarderContent'] != None:
                data['转发内容'] += item['forwarderContent']

        # 图像识别
        if 'ocrContents' in item.keys():
            if item['ocrContents'] != None:
                data['转发内容'] += item['ocrContents']

        if item['customFlag1'] == '5':
            data['positive_prob_number'] = 0.65
        # 非敏感
        elif item['customFlag1'] == '4':
            data['positive_prob_number'] = 0.9
        # 敏感
        elif item['customFlag1'] == '2':
            data['positive_prob_number'] = 0.1
        else:
            data['positive_prob_number'] = 0.9
        if len(data['标题'])<2:
            if len(data['描述'])>10:
                data['标题']=data['描述'][:10]
            else:
                data['标题'] = data['描述']
        # data['转发内容']='<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;' \
        #             'white-space: -pre-wrap;white-space: -o-pre-wrap; ' \
        #             'word-wrap: break-word;"><zhengwen>'+data['转发内容']+"</zhengwen></pre>"
        data['转发内容']=ex(data['转发内容'])
        data['标题'] = ex(data['标题'])[0:50]
        data_list.append(data)
    return data_list


def xpath_page_source(ch, method, properties, body):
    """
    解析数据
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """

    str_data = body.decode('utf-8')
    # str_data=str_data.replace("true","True").replace("false","False")
    dict_data = eval(str_data)
    list_data = _parse(dict_data['page_source_data'], dict_data['info']['id'])
    logger.info("解析完毕")

    # 将源码传入抓取队列，进行抓取
    clear_data_put = {
        'data': list_data,
        'info': dict_data['info'],
        'datacenter_id': dict_data['datacenter_id']
    }
    logger.info("解析源码完毕，进行发送")
    channel.basic_publish(exchange='',
                          routing_key=f'{queue_name}_clear_data',
                          body=str(clear_data_put),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )
                          )
    # 手动应答，效率会降低
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=f'{queue_name}_xpath',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,  # 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=xpath_page_source)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
