# -*- coding: utf-8 -*-
"""
   File Name：     ssql_helper_test
   Description :
   Author :       hike
   time：          2021/5/7 11:03
"""
from datetime import datetime
from utils.snowflake import IdWorker
import redis
import re
import requests
from utils.email_helper import my_Email
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
# 查看本次抓取插入到数据库内的数量
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
def find_info_count_B(start_time, end_time, C_Id):

    sql = "select count(*) from TS_DataMerge_Base where C_Id={C_Id} and PublishDate_Std between '{start_time}' and '{end_time}' ".format(
         C_Id=C_Id,start_time=start_time, end_time=end_time)

    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time>='2021-04-02 10:00:00' and create_time<='2021-04-02 11:00:00'"
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-04-02 10:00:00' and '2021-04-02 11:00:00' "
    # print(sql)
    # sql="select count(*) from dbo.TS_industry_news_circulation where create_time between '2021-03-22' and '2021-04-01' "
    count=db_qbbb.execute_query(sql)[0][0]
    # print(type(cursor.fetchall()))
    return count

# B库中查询客户名称以及行业名称 对应的关键词  使用服务器的数据库
def get_industry_keywords():
    # 查询所有启用项目
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
                        if d_a and i == 2:
                            new_d['excludewords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
                        if d_a and i == 1:
                            new_d['simultaneouswords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'

            if i == 1:
                new_d['customer'] = (d[1].encode('latin1').decode('gbk'))
            else:
                new_d['industry_name'] = (d[2].encode('latin1').decode('gbk'))
        new_d['keywords']=new_d['keywords'][:-1]
        new_d['excludewords']=new_d['excludewords'][:-1]
        new_d['simultaneouswords']=new_d['simultaneouswords'][:-1]
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
    # print(tuple_data_list_ts_a)
    db_a.execute_many(sql_ts_a, tuple_data_list_ts_a)
    # 二级数据表
    # print(tuple_data_list_ts_a_second_data)
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

    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    industry_id = db_b.execute_query(sql_industry_id)[0][0]
    new_data_list = []
    # redis滤重
    for data in datalist:
        if (r.sismember(industry_id, data['链接']) == False):
            new_data_list.append(data)
    print("rediss 滤重之后的数量")
    print(len(new_data_list))
    return new_data_list


def record_log(data):
    """
    数据记录
    """
    # A库 每一次抓取的记录
    sql_record = "insert into record_log_table values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # data=('3', '2021-4-26 00:00:00','2021-4-26 00:00:00', '2021-4-26 00:00:00', '4', '5', '6', '1')
    db_a.execute(sql_record,data)
    my_e = my_Email()
    if data[4]!=0 and data[5]!=0:
        if(data[5]/data[4])<0.7:
            my_e.send_message('数据量异常', data[6])
    elif data[4]==0 or data[5]==0:
        my_e.send_message('数据量异常', data[6])
    today=data[2].date()
    sql_industry_num = """
            if not exists (select * from record_log_industry  where industry = '{0}' and record_time='{1}')
                    INSERT INTO record_log_industry (industry,record_time,upload_num) VALUES ('{0}','{1}',{2})
                else
                    UPDATE record_log_industry SET upload_num=upload_num+{2}

                   WHERE industry = '{0}' and record_time='{1}'
            """.format(data[0], today, data[5])

    # 行业数据表每天增加
    # print(sql_industry_num)
    db_a.execute(sql_industry_num)
    print("Finash record")
    # pass

def customer_log():
    """
    统计项目数据量
    B库
    """
    for customer in get_industry_keywords():
        date_now=datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        date_yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

        sql_qbbb="select count(*) from TS_DataMerge_Base where C_Id='{0}' and PublishDate_Std between '{2}' and '{1}'".format(customer['id'],date_now,date_yesterday)
        # qbbb 库查询的数量
        today_customer_num=db_qbbb.execute_query(sql_qbbb)[0][0]
        # 记录项目的数据量
        sql_tsa_customer="insert into record_log_customer (customer,record_time,upload_num) values(%s,%s,%s)"
        data=(customer['customer'],date_yesterday,today_customer_num)
        db_a.execute(sql_tsa_customer,data)








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
    print(find_info_count_B('2021-05-19 13:00:00','2021-05-19 14:00:00',1387697657920643074))
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
    # for d in db_net_a.execute_query("select * from TS_test"):
    #     print(d)