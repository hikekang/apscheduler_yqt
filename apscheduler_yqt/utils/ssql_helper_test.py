# -*- coding: utf-8 -*-
"""
   File Name：     ssql_helper_test
   Description :
   Author :       hike
   time：          2021/5/7 11:03
"""
import json
import threading
from datetime import datetime
from fake_useragent import UserAgent
from utils.snowflake import IdWorker
import redis
import time
import re
import stomp
from utils.getdatabyselenium import get_num_driver
import requests
from utils import extract_content
from utils.ssql_pool_helper import DataBase,config_A,config_B,config_QBBA,config_QBBB,config_net_TS_A,config_net_QBBA
from utils.redis_helper import my_redis
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
config = {
    'server': '223.223.180.9',
    'user': 'tuser1',
    'password': 'tsuser1@123aA',
    'database': 'TS_A',
    'port': '39999'
}
db_a = DataBase('sqlserver',config_A)
db_b=DataBase('sqlserver',config_B)
db_qbba=DataBase('sqlserver',config_QBBA)
db_qbbb=DataBase('sqlserver',config_QBBB)
db_net_a=DataBase('sqlserver',config_net_TS_A)
db_net_qbba=DataBase('sqlserver',config_net_QBBA)

'''
优速 流通贸易
一嗨  汽车业
'''
tables = {
    "餐饮业": "dbo.TS_industry_news_catering",
    "保险业": "dbo.TS_industry_news_insurance",
    "房地产": "dbo.TS_industry_news_estate",
    "服务业": "dbo.TS_industry_news_service",
    "公关传统": "dbo.TS_industry_news_PR",
    "化妆品": "dbo.TS_industry_news_cosmetic",
    "IT业": "dbo.TS_industry_news_IT",
    "教育": "dbo.TS_industry_news_education",
    "金融业": "dbo.TS_industry_news_financial",
    "机械制造": "dbo.TS_industry_news_machine",
    "快消品": "dbo.TS_industry_news_FMCG",
    "流通贸易": "dbo.TS_industry_news_circulation",
    "旅游业": "dbo.TS_industry_news_tourism",
    "汽车业": "dbo.TS_industry_news_automotive",
    "食品业": "dbo.TS_industry_news_food",
    "文化出版": "dbo.TS_industry_news_cultural",
    "医疗保健": "dbo.TS_industry_news_medical",
    "其它": "dbo.TS_industry_news_other",
}

def find_info_count(start_time, end_time, industry_name):
    table_name = tables[industry_name]
    sql = "select count(*) from {table_name} where publish_time between '{start_time}' and '{end_time}' ".format(
        table_name=table_name, start_time=start_time, end_time=end_time)

    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time>='2021-04-02 10:00:00' and create_time<='2021-04-02 11:00:00'"
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-04-02 10:00:00' and '2021-04-02 11:00:00' "
    # print(sql)
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-03-22' and '2021-04-01' "
    count=db_a.execute_query(sql)[0][0]
    # print(type(cursor.fetchall()))
    return count

# B库中查询客户名称以及行业名称 对应的关键词  使用服务器的数据库
def get_industry_keywords():
    sql_qbbb = "select * from TS_Customers where IsEnable=1"
    # get enable project
    data = db_qbbb.execute_query(sql_qbbb)
    new_data = []
    for d in iter(data):
        # 处理乱码
        new_d = {
            'id': '',  # 客户id
            'customer': '',  # 项目
            'industry_name': '',  # 行业名称
            'keywords': '',  # 关键词
            'excludewords': '',  # 排除词
            'simultaneouswords': '',  # 同现词
        }
        # principals
        for i, dd in enumerate(d):
            if i == 0:
                new_d['id'] = dd
                # 单字段去重
                sql_QBBA = "select Word,SimultaneousWord,Excludeword from QBB_A.dbo.TS_Keywords where C_ID={} " \
                           "group by Word,SimultaneousWord,Excludeword".format(dd)

                data_A = db_qbba.execute_query(sql_QBBA)
                for da in data_A:
                    for i, d_a in enumerate(da):
                        if d_a and i == 0:
                            new_d['keywords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
                        if d_a and i == 1:
                            new_d['excludewords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
                        if d_a and i == 2:
                            new_d['simultaneouswords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
            if i == 1:
                new_d['customer'] = (d[1].encode('latin1').decode('gbk'))
            else:
                new_d['industry_name'] = (d[2].encode('latin1').decode('gbk'))
        new_data.append(new_d)
    new_eight = []
    for word in new_data:
        new_d = {
            'id': '',  # 客户id
            'customer': '',  # 项目
            'industry_name': '',  # 行业名称
            'keywords': '',  # 关键词
            'excludewords': '',  # 排除词
            'simultaneouswords': '',  # 同现词
        }
        if word['industry_name'] in '流通贸易、服务业、教育、文化':
            new_d = word
            new_d['industry_name'] = '流通贸易'
            new_eight.append(new_d)
        if word['industry_name'] in '金融、保险业':
            new_d = word
            new_d['industry_name'] = '金融业'
            new_eight.append(new_d)
        if word['industry_name'] in '软件、数码产品、IT业':
            new_d = word
            new_d['industry_name'] = 'IT业'
            new_eight.append(new_d)
        if word['industry_name'] in '房地产、建材、工程':
            new_d = word
            new_d['industry_name'] = '房地产'
            new_eight.append(new_d)
        if word['industry_name'] in '汽车业、机械制造':
            new_d = word
            new_d['industry_name'] = '汽车业'
            new_eight.append(new_d)
        if word['industry_name'] in '快消品、餐饮业、食品、医疗':
            new_d = word
            new_d['industry_name'] = '快消品'
            new_eight.append(new_d)
        if word['industry_name'] in '化妆品、服装':
            new_d = word
            new_d['industry_name'] = '化妆品'
            new_eight.append(new_d)
        if word['industry_name'] in '娱乐、旅游':
            new_d = word
            new_d['industry_name'] = '旅游业'
            new_eight.append(new_d)
    # for d in new_eight:
    #     print(d)
    return new_eight


def merger_industry_data(list_msg):
    """
    同一个行业的项目关键词进行合并
    """
    set_mark = {i['industry_name'] for i in list_msg}
    # 设置动态命名模板
    list_name_template = 'list_data_'
    # 创建local对象，准备创建动态变量
    createver = locals()
    # 循环遍历数据并创建动态列表变量接收
    for mark in set_mark:
        # 动态创建变量
        createver[list_name_template + mark.replace('-', '_')] = [dict_current for dict_current in list_msg if
                                                                  dict_current['industry_name'] == mark]
    n_d = []
    for name in set_mark:
        # print(list_name_template + name + ':', end='\t')  # 打印自动创建的变量名称，采用tab分隔
        # exec('print(' + list_name_template + name + ')')  # 打印变量内容（列表）
        exec('n_d.append(' + list_name_template + name + ')')  # 打印变量内容（列表）
    n_e_d=[]
    for industry_word in n_d:
        # print(industry_word)
        words=''
        for i,word in enumerate(industry_word):
            if i!=0:
                industry_word[0]['keywords']+=word['keywords']
                industry_word[0]['customer']+="_"+word['customer']
                industry_word[0]['excludewords']+=word['excludewords']
                industry_word[0]['simultaneouswords']+=word['simultaneouswords']
                # industry_word[0][]
        n_e_d.append(industry_word[0])
    # 八个行业

    return n_e_d



def post_data(data_list, industry_name):
    """
    单数据插入
    """

    table_name = tables[industry_name]
    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    # print(sql_industry_id)
    # sql_industry_id="select id from TS_Industry wh"
    industry_id = db_b.execute_query(sql_industry_id)[0][0]
    print(len(data_list))
    for data in data_list:
        worker = IdWorker(1, 2, 0)
        # 生成雪花id
        id = worker.get_id()
        # positive_prob=baidu_emition.emotion(data['转发内容'][0:1000])
        # time.sleep(0.3)
        sql_ts_a = "insert into %s (id,industry_id,title,summary,content,url,author,publish_time,emotion_status,ic_id,keywords_id) values (%d,%d,'%s','%s','%s','%s','%s','%s',%f,%s,%s)" % (
        table_name, id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'], data['时间'],data['positive_prob_number'],data['ic_id'],data['keywords_id'])
        sql_qbb_a = "insert into %s (id,industry_id,title,summary,content,url,author,publish_time,is_original,location,emotion_status) values " \
                    "(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%f,%s,%s)" % (table_name, id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'],
                    data['时间'], data['is_original'], data['area'], data['positive_prob_number'],data['ic_id'],data['keywords_id'])
        # 插入A库
        db_a.execute(sql_ts_a)
        datas = {
            "id": id,
            "industryId": industry_id
        }
        # 更新redis
        r.sadd(industry_id, data['链接'])

        # 滤重
        # post_mq.send_to_queue('reptile.stay.process',str(data))
        # print("执行")
        # 插入QBB_A库
        db_qbba.execute(sql_qbb_a)
        # 拉取信息到B库
        # post_mq.send_to_queue('reptile.stay.process_2.1',str(data))

        params = {
            'queues': 'reptile.stay.process_2.1',
            'message': datas
        }
        # print(params)
        url = 'http://localhost:8090/jms/send?queues=%s&message={"id":%s,"industryId":%s}' % (
        'reptile.stay.process_2.1', id, industry_id)
        # requests.get('http://localhost:8090/jms/send',params=params)
        # print(url)
        proxies = {'http': None, 'https': None}
        # proxies = {"http": None, "https": None}
        requests.get(url, proxies=proxies)
    print("数据上传成功")


def upload_many_data(data_list, industry_name):
    """
    多数据插入

    """
    myredis = my_redis()
    table_name = tables[industry_name]
    # 查询hangyeid
    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    industry_id = db_b.execute_query(sql_industry_id)[0][0]

    tuple_data_list_ts_a = []
    tuple_data_list_ts_a_second_data = []
    tuple_data_list_qbb_a = []
    post_data_list = []
    worker = IdWorker(1, 2, 0)
    for data in data_list:
        # 生成雪花id

        id = worker.get_id()
        post_data = {
            "id": id,
            "industryId": industry_id  # 行业id
        }
        post_data_list.append(post_data)
        # 更新redis
        myredis.redis.sadd(industry_id, data['链接'])

        tuple_data_ts_a = (
            id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'], data['时间'],
            data['positive_prob_number'])



        tuple_data_qbb_a = (
            id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'], data['时间'],
            data['is_original'], data['area'], data['positive_prob_number'])

        tuple_data_list_ts_a.append(tuple_data_ts_a)

        tuple_data_list_qbb_a.append(tuple_data_qbb_a)

        tuple_data_ts_a_second_data = (id, industry_id, data['ic_id'], data['keywords_id'], data['链接'])
        tuple_data_list_ts_a_second_data.append(tuple_data_ts_a_second_data)

    sql_ts_a_second_data="insert into TS_Second_Data (id,industry_id,ic_id,keywords_id,url) values (%d,%d,%s,%s,%s)"
    sql_ts_a = "insert into " + table_name + " (id,industry_id,title,summary,content,url,author,publish_time,emotion_status) values (%d,%d,%s,%s,%s,%s,%s,%s,%s)"
    # 插入A库
    sql_qbb_a = "insert into " + table_name + " (id,industry_id,title,summary,content,url,author,publish_time,is_original,location,emotion_status) values (%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print(tuple_data_list_ts_a)
    db_a.execute_many(sql_ts_a, tuple_data_list_ts_a)
    # 二级数据表
    print(tuple_data_list_ts_a_second_data)
    db_a.execute_many(sql_ts_a_second_data, tuple_data_list_ts_a_second_data)

    db_net_a.execute_many(sql_ts_a, tuple_data_list_ts_a)
    db_qbba.execute_many(sql_qbb_a, tuple_data_list_qbb_a)
    db_net_qbba.execute_many(sql_qbb_a, tuple_data_list_qbb_a)

    # 消息队列
    data_2_1 = {
        'queues': 'reptile.stay.process_2.1',
        'message': str(post_data_list)
    }
    data_2 = {
        'queues': 'reptile.stay.process',
        'message': str(post_data_list)
    }

    proxies = {'http': None, 'https': None}
    url = 'http://localhost:8090/jms/send_array'
    requests.get(url=url, proxies=proxies, params=data_2_1)
    requests.get(url=url, proxies=proxies, params=data_2)
    print("数据上传成功")
    myredis.close()
def testsql():
    """
     测试sql语句

    """
    sql_ts_a = "insert into '%s' (id,industry_id,title,summary,content,url,author,publish_time) values (''%s'','%s','%s','%s','%s','%s','%s','%s')" % (
    'hike', 'hike', 'hike', 'hike', 'hike', 'hike', 'hike', 'hike', 'hike',)
    print(sql_ts_a)
    # 插入A库
    # sql_record = "insert into record_log_table (industry,crawl_time,start_time,end_time,yqt_num,crawl_num,upload_num,customer) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % ('1', '2021-4-26 00:00:00', '2021-4-26 00:00:00', '2021-4-26 00:00:00', '1', '1', '1', '1')
    sql_record = "insert into record_log_table values ('%s','%s','%s','%s','%s','%s','%s','%s')" % ('1', '2021-4-26 00:00:00', '2021-4-26 00:00:00', '2021-4-26 00:00:00', '1', '1', '1', '1')
    db_a.execute(sql_record)



def get_month_data(time1, time2):
    """
    # 将所有行业的数据加载到内存中
    """
    myredis = my_redis()

    myredis.redis.flushall()
    for tb in tables.values():
        sql = "select industry_id,url from %s where publish_time between '%s' and '%s'" % (tb, time1, time2)
        print(sql)
        datas = db_a.execute_query(sql)
        for d in datas:
            myredis.redis.sadd(d[0], d[1])
    myredis.close()


# 根据url进行二次滤重
def filter_by_url(datalist, industry_name):
    """

    """

    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    industry_id = db_b.execute_query(sql_industry_id)[0][0]
    new_data_list = []
    # redis滤重
    for data in datalist:
        print(data['链接'])
        if (r.sismember(industry_id, data['链接']) == False):
            new_data_list.append(data)
    print("rediss 滤重之后的数量")
    print(len(new_data_list))
    return new_data_list
def record_log(data):
    """
    数据记录
    """
    sql_record = "insert into record_log_table values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # data=('3', '2021-4-26 00:00:00','2021-4-26 00:00:00', '2021-4-26 00:00:00', '4', '5', '6', '1')
    db_a.execute(sql_record,data)
    # pass


def get_teack_datas():
    """
    数据库中获取追踪的url
    """
    sql_of_extend = "select SN from TS_DataMerge_Extend where is_Track=1"
    datas = db_qbbb.execute_query(sql_of_extend)
    url_list = []
    for data in datas:
        sql_of_base = "select URL from TS_DataMerge_Base where SN='%s'" % (data[0])
        urls = db_qbbb.execute_query(sql_of_base)
        if "weibo.com" in urls[0]:
            url = {
                'sn': data[0],
                'url': urls[0]
            }
            url_list.append(url)
    return url_list

def get_track_datas_qbbb():
    """
    数据库qbbb,track_task中获取数据
    """
    sql="select * from TS_track_task where is_done=0"
    db_qbbb.execute(sql)
    datas=db_qbbb.execute_query()
    return datas

def second_data_url_sql():
    """
    二层数据抓取 url查询
    """
    sql="select * from TS_Second_Data where crawl_flag=0"
    data=db_a.execute_query(sql)
    return data

def crawl_data(data):
    """
    抓取二层数据并进行更新数据库
    """
    url = 'http://yuqing.sina.com/newEdition/getDetail.action'
    headers = {
        'User-Agent': UserAgent().random,
        'Cookie': 'Hm_lvt_d535b0ca2985df3bb95f745cd80ea59e=1619337563,1619416119,1619494308,1619574875; Hm_lpvt_d535b0ca2985df3bb95f745cd80ea59e=1619574875; Hm_lvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619337563,1619416119,1619494308,1619574875; Hm_lpvt_c29f5cd9e2c7e8844969c899f7ac90d3=1619574875; www=userSId_yqt365_hbslxx_239715_72496; JSESSIONID=53D37416EB6EA584070A2EAFCE70E515'
    }
    params = {
        'icc.id': data[2],
        'kw.keywordId':data[3]
    }
    r=requests.post(url,params=params,headers=headers,proxies = {'http': None, 'https': None})
    time.sleep(0.3)
    print(r.text)
    data_content = json.loads(r.text)
    print(data_content)
    # 获取数据
    content=extract_content.extract_content(str('<html><body>'+data_content['icc']['content']))
    # print(content+"\n")
    # B库更新
    sql_Base = "update TS_DataMerge_Base set Body='%s'where url='%s' "% (content,data[5])
    print(sql_Base)
    db_qbbb.execute(sql_Base)

    sql_second_data="update TS_Second_Data set crawl_flag=1 where url='%s'"%data[5]
    db_a.execute(sql_second_data)

def multi_thread():
    """
    多线程数据爬取
    """
    threads=[]
    for data in iter(second_data_url_sql()):
        threads.append(
            threading.Thread(target=crawl_data,args=(list(data),))
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def single_thread():
    for data in iter(second_data_url_sql()):
        crawl_data(data)


def track_data_task():
    """
    直接扫描表
    数据库中获取链接进行追踪
    """
    driver=get_num_driver()
    for data in get_track_datas_qbbb():

        num = driver.get_data_it(data[1])
        create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     转发、评论、点赞
        # 追踪记录
        sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
        data[2], num[0], num[1], num[2], create_date)
        db_qbbb.execute(sql_record)
        # 更新值
        sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
        num[0], num[1], num[2], data[2])
        db_qbbb.execute(sql_Base)
        # print('更新库')
         #     修改数据追踪表
        sql_track_task="update TS_track_task set is_done=1 where sn='%s' "%data[2]
        db_qbbb.execute(sql_track_task)
        # print('追踪完毕')
    driver.close()


def track_data_number_sql2(sn, data):
    """
    stomp版本
    将得到的数据插入数据库
    """
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     转发、评论、点赞
    sql_record = "insert into TS_track_record(sn,forward_num,comment_num,good_num,create_date) values('%s','%d','%d','%d','%s')" % (
    sn, data[0], data[1], data[2], create_date)
    db_qbbb.execute(sql_record)
    sql_Base = "update TS_DataMerge_Base set Transpond_Num=%d,Comment_Num=%d,Forward_Good_Num=%d where SN='%s' " % (
    data[0], data[1], data[2], sn)
    db_qbbb.execute(sql_Base)


# track_data_number_sql()


# ----------------------------数据追踪消息队列------------------------------------------------


class MyListener(stomp.ConnectionListener):
    """
    自己的监听队列，操作数据库
    """
    def __init__(self,conn):
        self.conn = conn
        self.msg_list=[]

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        pattern = re.compile(r'http://weibo.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        url = re.findall(pattern, frame.body)
        if url:
            self.msg_list.append(frame.body)
            print("处理之后的链接：" + url[0])
            # # 爬取评论转发点赞数量
            # data = get_data_it(url[0])
            # sn = frame.body.split('"')[3]
            # track_data_number_sql2(sn, data)
            # for x in range(5):
            #     print(x)
            #     time.sleep(1)
            # print('processed message')
            # print("监听的url：" + url[0])
        print(self.msg_list)
    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)
    def get_msg_list(self):
        print(self.msg_list)
        return self.msg_list

def connect_and_subscribe(conn):
    """
    连接和监听
    """
    conn.connect('admin', 'admin', wait=True)
    conn.subscribe(destination='task.msg.tracker_2.1', id=1, ack='auto')


def re_connect_subscribe(conn):
    """
    重新登记注册
    :return:
    """
    conn.disconnect()
    time.sleep(3)
    connect_and_subscribe(conn)

def get_url_from_stomp(frame_body_list):
    try:
        if frame_body_list:
            print("开始抓数据")
            for frame_body in frame_body_list:
                pattern = re.compile(r'http://weibo.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                url = re.findall(pattern, frame_body)
                driver=get_num_driver()
                data = driver.get_data_it(url[0])
                sn = frame_body.split('"')[3]
                track_data_number_sql2(sn, data)
                for x in range(3):
                    print(x)
                    time.sleep(1)
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        driver.close()


def track_data_work():
    conn = stomp.Connection(host_and_ports=[('223.223.180.10', 61613)],heartbeats=(4000, 4000))
    # conn.connect('admin', 'admin', wait=True)
    lst = MyListener(conn)
    # lst = MyListener()
    conn.set_listener('track_data', lst)
    connect_and_subscribe(conn)
    conn.unsubscribe(destination='task.msg.tracker_2.1', id=1, ack='auto')
    time.sleep(2)
    frame_body_list=lst.get_msg_list()
    print(frame_body_list)
    # conn.disconnect()
    # conn.disconnect()
    hike_flag=get_url_from_stomp(frame_body_list)
    if hike_flag:
        return  track_data_work()
    else:
        conn.disconnect()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


if __name__ == '__main__':
    # while 1:
    # track_data_work()
    # multi_thread()

    # single_thread()

    # for d in get_industry_keywords():
    #     print(d)
    # track_data_task()
    # record_log()

    # for d in merger_industry_data(get_industry_keywords()):
    #     print(d)
    # get_industry_keywords()
    # sql_QBBB = "select * from TS_Customers where IsEnable=1"

    # db_qbbb.execute_query(sql_QBBB)
    # db_a.execute_query("select * from crawler_word")
    # for data in get_track_datas():
    #     print(data)
    # track_data_task()

    # for data in second_data_url_sql():
    #     print(data)
    #     print(data[5])
    for d in db_net_a.execute_query("select * from TS_test"):
        print(d)