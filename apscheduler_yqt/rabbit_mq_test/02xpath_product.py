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
import re
from lxml import etree
import time
from utils.mylogger import logger

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='xpath', durable=True)
channel.queue_declare(queue='clear_data', durable=True)


def _parse(page_source, info_id):
    p = re.compile("r'\s*|\t|\r|\n'")
    doc = etree.HTML(page_source)
    item_trs = doc.xpath('.//tr[@class="ng-scope"]')
    time.sleep(0.2)
    data_list = []
    for tr in item_trs[1:]:
        tds = tr.xpath('.//td')
        # 内容
        article_id = tds[0].xpath('.//input')[0].get('id').split("_")[-1]
        td_title = tds[1]
        # 来源
        td_orgin = tds[3]
        # 文章站点
        site_name = td_orgin.xpath('span')[0].text

        # 文章时间
        td_time = tds[4].xpath('.//span[@class="date"]/text()')

        def parse_time(td_time):
            from datetime import datetime
            ymd_1 = p.sub("", td_time[0])
            ymd_2 = p.sub("", td_time[1])
            try:
                if "年" in ymd_1:  # 不是今年的数据
                    ymd = "".join([ymd_1, ymd_2])
                elif "今天" in ymd_2:  # 今天的数据
                    ymd = " ".join([f"{str(datetime.now().date())}", ymd_1])
                    return datetime.strptime(ymd, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                else:
                    ymd = " ".join([f"{datetime.now().year}年" + ymd_2, ymd_1])
                return datetime.strptime(ymd, "%Y年%m月%d日 %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logger.warning(e)
                logger.warning(td_time)

        # 转发类型  原创 有一部分是没有的 在这里只进行微博的判断
        if site_name == "新浪微博":
            # sort_1 = td_title.xpath('.//span[contains(@ng-if,"icc.repostsFlg!=0")]/text()')
            sort_1 = td_title.xpath('.//span[contains(@ng-if,"icc.repostsFlg")]')[0].get('ng-if')
            if sort_1 == "icc.repostsFlg==0":
                sort = "原创"
            else:
                sort = "转发"
            # if len(sort_1) > 0:
            #     sort = p.sub("", sort_1[0])
            # else:
            #     sort = "原创"
        else:
            sort = "原创"

        # 获取内容所有文本
        content = p.sub("",
                        td_title.xpath('.//div[contains(@class,"item-title news-item-title contenttext ng-binding")]')[
                            0].xpath(
                            'string(.)'))
        # 获取转发内容的所有文本
        spread = td_title.xpath('.//div[contains(@class,"should-spread-area")]')
        spread_content = ''
        if spread:
            spread_content = p.sub("", spread[0].xpath('string(.)'))
        else:
            spread_content = ''
        # 针对于文章是标题  针对于微博是作者
        author = td_title.xpath('.//div[contains(@class,"profile-title inline-block")]/a')[0].xpath(
            'string(.)').replace("\n", "")
        author_or_title = p.sub("", author)
        title = ''
        if site_name == '新浪微博':
            author = author_or_title
        else:
            title_pattern = re.compile('(.*)[:|：](.*)')
            title_match = title_pattern.findall(author_or_title)
            if len(title_match) > 0:
                if len(title_match[0]) > 1:
                    author = title_match[0][0]
                    title = ''.join(title_match[0][1:])
                else:
                    author = ''
                    title = title_match[0][0]
            else:
                author = ''
                title = author_or_title
        title1 = ''
        if site_name == '新浪微博':
            author1 = author_or_title
        else:
            result_a_t = author_or_title.split(":")
            result_a_t_1 = author_or_title.split("：")

            if len(result_a_t) >= 2:
                author1 = result_a_t[0]
                title1 = ''.join(result_a_t[1:])
            elif len(result_a_t_1) >= 2:
                author1 = result_a_t_1[0]
                title1 = ''.join(result_a_t_1[1:])
            else:
                author1 = ''
                if result_a_t_1:
                    title1 = result_a_t_1[0]
                if result_a_t:
                    title1 = result_a_t[0]
        # 行业
        # industry = p.sub("", td_title.xpath('.//div[@class="profile-tip inline-block"]/nz-tag[2]/span/text()')[0])
        # 关键词
        relate_words = "【关键词：】" + p.sub("", td_title.xpath('.//span[@ng-bind="icc.referenceKeyword"]')[0].xpath(
            'string(.)')) + "\n"
        attitude = p.sub("", td_title.xpath(
            './/div[contains(@class,"sensitive-status-content") and not(contains(@class,"ng-hide"))]')[0].xpath(
            ".//span")[0].text)
        title_time = parse_time(td_time)

        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        title = highpoints.sub('', title).replace(" ", "").replace("\n", "")
        content = highpoints.sub(u'', content).replace(" ", "").replace("\n", "")
        source_url = td_title.xpath('.//div[@class="btn-group inline-block"]/ul/li[4]/a/@href')[0]
        title_author_re = re.compile('\s+')
        author = re.sub(title_author_re, "", author)

        title = re.sub(title_author_re, "", title)
        author1 = re.sub(title_author_re, "", author1)
        title1 = re.sub(title_author_re, "", title1)
        print("---" * 20)
        print(author_or_title)
        print("作者:%s\n标题：%s" % (author, title))
        print("***" * 20)
        print("作者:%s\n标题：%s" % (author1, title1))
        print("转发原创类型：", sort, source_url)
        data = {
            '时间': title_time,
            '标题': title if title != '' else content,
            '描述': content,  # 微博原创
            '链接': source_url,
            '转发内容': '<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;' \
                    'white-space: -pre-wrap;white-space: -o-pre-wrap; ' \
                    'word-wrap: break-word;"><zhengwen>' + spread_content + content + "</zhengwen></pre>",
            '发布人': author,
            'attitude': attitude,
            'sort': sort,
            'related_words': relate_words,
            'site_name': site_name,
            'area': p.sub("", td_orgin.xpath('.//div[contains(@ng-if,"icc.province")]')[0].text),
            # 'C_Id': self.info['id'],  # 客户id
            'C_Id': info_id,  # 客户id
            'article_id': article_id
        }
        positive_dict = {
            "敏感": 0.1,
            "非敏感": 0.9,
            "中性": 0.65
        }
        data['positive_prob_number'] = positive_dict[attitude.split()[0]]
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
    dict_data = eval(str_data)
    list_data = _parse(dict_data['page_source'], dict_data['info']['id'])
    print("解析完毕")

    # 将源码传入抓取队列，进行抓取
    clear_data_put = {
        'data': list_data,
        'info': dict_data['info'],
        'datacenter_id': dict_data['datacenter_id']
    }
    print("解析源码完毕，进行发送")
    channel.basic_publish(exchange='',
                          routing_key='clear_data',
                          body=str(clear_data_put),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )

                          )
    # 手动应答，效率会降低
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='xpath',
                      # auto_ack=True,# 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      auto_ack=False,  # 默认应答，很可能因为回调函数造成数据丢失，改为手动应答
                      on_message_callback=xpath_page_source)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
