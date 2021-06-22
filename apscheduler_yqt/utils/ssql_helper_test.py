# -*- coding: utf-8 -*-
"""
   File Name：     ssql_helper_test
   Description :   使用数据库连接池进行操作
   Author :       hike
   time：          2021/5/7 11:03
"""
from utils.snowflake import IdWorker
import redis
import re
import requests
from utils.email_helper import my_Email
from utils.ssql_pool_helper import DataBase, config_A, config_B, config_QBBA, config_QBBB, config_net_TS_A, \
    config_net_QBBA
from utils.redis_helper import my_redis
from tqdm import tqdm
import uuid
from utils import domain
# from datetime import datetime
import datetime
from urllib import parse
from utils import post_mq
from pprint import pprint

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
config = {
    'server': '223.223.180.9',
    'user': 'tuser1',
    'password': 'tsuser1@123aA',
    'database': 'TS_A',
    'port': '39999'
}
db_a = DataBase('sqlserver', config_A)
db_b = DataBase('sqlserver', config_B)
db_qbba = DataBase('sqlserver', config_QBBA)
db_qbbb = DataBase('sqlserver', config_QBBB)
db_net_a = DataBase('sqlserver', config_net_TS_A)
tables = {

    # 1.流通贸易
    "流通贸易": "dbo.TS_industry_news_circulation",
    "服务业": "dbo.TS_industry_news_service",
    "教育": "dbo.TS_industry_news_education",
    "文化出版": "dbo.TS_industry_news_cultural",

    # 2.金融业
    "金融业": "dbo.TS_industry_news_financial",
    "保险业": "dbo.TS_industry_news_insurance",

    # 3.IT业
    "IT业": "dbo.TS_industry_news_IT",

    # 4.房地产
    "房地产": "dbo.TS_industry_news_estate",



    # 5.汽车业
    "汽车业": "dbo.TS_industry_news_automotive",
    "机械制造": "dbo.TS_industry_news_machine",

    # 6.快消品
    "快消品": "dbo.TS_industry_news_FMCG",
    "餐饮业": "dbo.TS_industry_news_catering",
    "食品业": "dbo.TS_industry_news_food",
    "医疗保健": "dbo.TS_industry_news_medical",

    # 7.化妆品
    "化妆品": "dbo.TS_industry_news_cosmetic",

    # 8.旅游业
    "旅游业": "dbo.TS_industry_news_tourism",

    "公关传统": "dbo.TS_industry_news_PR",
    "其它": "dbo.TS_industry_news_other",
}
db_net_qbba = DataBase('sqlserver', config_net_QBBA)

'''
优速 流通贸易
一嗨  汽车业
'''

def find_curent_num(start_time, end_time, myconfig,info,yqt_count):
    """
    查看本次抓取插入到数据库内的数量
    :param start_time:开始时间
    :param end_time:结束时间
    :param industry_name:行业名称
    :return:
    """
    industry_name=myconfig.getValueByDict('industry_info', 'industry_name')
    table_name = tables[industry_name]
    sql_A = "select count(*) from {table_name} where publish_time between '{start_time}' and '{end_time}' ".format(
        table_name=table_name, start_time=start_time, end_time=end_time)

    count_A = db_a.execute_query(sql_A)[0][0]
    sql_B = "select count(*) from TS_DataMerge_Base where " \
            "C_Id={C_Id} and PublishDate_Std between '{start_time}' and '{end_time}' ".format(
        C_Id=info['id'], start_time=start_time, end_time=end_time)

    count_B = db_qbbb.execute_query(sql_B)[0][0]

    sql_record_log_customer="insert into record_log_customer (customer,record_time,yqt_num,TS_A_num,QBB_B_num) " \
                            "values (%s,%s,%d,%d,%d)"
    db_a.execute(sql_record_log_customer,(info['customer'],end_time,yqt_count,count_A,count_B))

    return count_A,count_B


def find_day_data_count(myconfig):
    """
    修改  行业报表不需要发给客户
    执行时间每天24:00执行一次
    查询一天行业抓取的数据量
    :param myconfig:项目配置
    :return:本次
    """

    # 开始时间和结束时间为一整天
    end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + "00:00:00"
    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + "00:00:00"
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    industry_name = myconfig.getValueByDict('industry_info', 'industry_name')

    p_data = []
    project_list = merger_industry_data(get_industry_keywords())
    for project_data in project_list:
        # if project_data['industry_name'] == '流通贸易':
        if project_data['industry_name'] == industry_name:
            p_data.append(project_data)
    industry_table_name = tables[industry_name]

    sql_A = "select count(*) from {} where publish_time between '{start_time}' and '{end_time}' ".format(
        industry_table_name, start_time=start_time, end_time=end_time)
    # 流通贸易这个行业在A库中的数据量
    count_A = db_a.execute_query(sql_A)[0][0]

    count_B=0
    # 根据C_Id查询B库中的数据量
    for item in p_data:
        sql_B = "select count(*) from TS_DataMerge_Base where " \
                "C_Id={C_Id} and PublishDate_Std between '{start_time}' and '{end_time}' ".format(
            C_Id=item['id'], start_time=start_time, end_time=end_time)

        count_B+= int(db_qbbb.execute_query(sql_B)[0][0])


    sql_insert_a = "insert into record_log_industry (industry,record_time,TS_A_num,QBB_B_num) values (%s,%s,%d,%d)"

    db_a.execute(sql_insert_a, (industry_name, end_time, count_A, count_B))

    # 插入记录

    return count_B


# B库中查询客户名称以及行业名称 对应的关键词  使用服务器的数据库

def get_industry_keywords():
    def replace_char1(string, char, index):
        string = list(string)
        string[index] = char
        return ''.join(string)
    # qbbb库查询所有启用项目
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
            'email':'',
            'yqt_keywords':'('
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
                            # new_d['keywords'] += re.sub('、', '|', d_a) + '|'
                            new_d['yqt_keywords']+="("+re.sub('、', '|', d_a.encode('latin1').decode('gbk'))
                        # if d_a and i == 2:
                        if d_a and i == 2:
                            new_d['excludewords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
                            # new_d['excludewords'] += re.sub('、', '|', d_a) + '|'

                        if d_a and i == 1:
                            new_d['simultaneouswords'] += re.sub('、', '|', d_a.encode('latin1').decode('gbk')) + '|'
                            new_d['yqt_keywords'] += "+("+re.sub('、', '|', d_a.encode('latin1').decode('gbk')) +"))|"
                            # new_d['simultaneouswords'] += re.sub('、', '|', d_a) + '|'
                        elif d_a==None and i==1:
                            new_d['yqt_keywords']+=")|"
                new_d['yqt_keywords']+=")"
                new_d['yqt_keywords']=replace_char1(new_d['yqt_keywords'],"",-2)
            if i == 1:
                new_d['customer'] = (d[1].encode('latin1').decode('gbk'))
                # new_d['customer'] = (d[1])
            elif i==2:
                new_d['industry_name'] = (d[2].encode('latin1').decode('gbk'))
                # new_d['industry_name'] = (d[2])
            elif i==7:
                new_d['email']=dd
        new_d['keywords'] = new_d['keywords'][:-1]
        new_d['excludewords'] = new_d['excludewords'][:-1]
        new_d['simultaneouswords'] = new_d['simultaneouswords'][:-1]
        new_data.append(new_d)
    new_eight = []
    # 八个行业项目
    for word in new_data:
        new_d = {
            'id': '',  # 客户id
            'customer': '',  # 项目
            'industry_name': '',  # 行业名称
            'keywords': '',  # 关键词
            'excludewords': '',  # 排除词
            'simultaneouswords': '',  # 同现词
            'email':''
        }
        if word['industry_name'] in '流通贸易、服务业、教育、文化出版':
            new_d = word
            new_d['industry_name'] = '流通贸易'
            new_eight.append(new_d)
        if word['industry_name'] in '金融业、保险业':
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
        if word['industry_name'] in '快消品、餐饮业、食品、医疗保健':
            new_d = word
            new_d['industry_name'] = '快消品'
            new_eight.append(new_d)
        if word['industry_name'] in '化妆品、服装':
            new_d = word
            new_d['industry_name'] = '化妆品'
            new_eight.append(new_d)
        if word['industry_name'] in '娱乐、旅游业、其它、公关传统':
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
    n_e_d = []
    for industry_word in n_d:
        # print(industry_word)
        words = ''
        for i, word in enumerate(industry_word):
            if i != 0:
                industry_word[0]['keywords'] += word['keywords']
                industry_word[0]['customer'] += "_" + word['customer']
                industry_word[0]['excludewords'] += word['excludewords']
                industry_word[0]['simultaneouswords'] += word['simultaneouswords']
                # industry_word[0][]
        n_e_d.append(industry_word[0])
    # 八个行业

    return n_e_d

def merger_industry_data_industry(list_msg):
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
    n_e_d = []
    for industry_word in n_d:
        # print(industry_word)
        words = ''
        for i, word in enumerate(industry_word):
            if i != 0:
                industry_word[0]['keywords'] += word['keywords']
                industry_word[0]['customer'] += "_" + word['customer']
                industry_word[0]['excludewords'] += word['excludewords']
                industry_word[0]['simultaneouswords'] += word['simultaneouswords']
                # industry_word[0][]
        n_e_d.append(industry_word[0])
    # 八个行业
    return n_e_d


def post_data(data_list, industry_name):
    """
    单数据插入
    """

    table_name = tables[industry_name]
    sql_industry_id = "select id from TS_Industry where name='" + table_name + "'"
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
            table_name, id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'], data['时间'],
            data['positive_prob_number'], data['ic_id'], data['keywords_id'])
        sql_qbb_a = "insert into %s (id,industry_id,title,summary,content,url,author,publish_time,is_original,location,emotion_status) values " \
                    "(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%f,%s,%s)" % (
                        table_name, id, industry_id, data['标题'], data['描述'], data['转发内容'], data['链接'], data['发布人'],
                        data['时间'], data['is_original'], data['area'], data['positive_prob_number'], data['ic_id'],
                        data['keywords_id'])
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



def contain_keywords(keywords, str):
    return any(k in str for k in keywords.split("、"))

def match_alone_keyword_(info, d):
    """

    :param info:关键词信息
    :param d:单条数据
    :return:
    """
    #
    print("单独进行匹配")


    match_data=d['标题'] + d['转发内容'] + d['描述']
    if info['keywords'] != '':
        if info['excludewords'] == '' and info['simultaneouswords'] == '':
            if contain_keywords(info['keywords'],match_data ):
                d['sort_num'] += 1
                if info['parent_id'] not in d['parent_id']:
                    d['parent_id'].append(info['parent_id'])
                    d['class_id'].append(info['class_id'])

        elif info['simultaneouswords'] != '' and info['excludewords'] == '':
            if contain_keywords(info['keywords'],match_data):
                if contain_keywords(info['simultaneouswords'], match_data):
                    d['sort_num'] += 1
                    if info['parent_id'] not in d['parent_id']:
                        d['parent_id'].append(info['parent_id'])
                        d['class_id'].append(info['class_id'])
        elif info['simultaneouswords'] == '' and info['excludewords'] != '':
            if contain_keywords(info['keywords'], match_data):
                if contain_keywords(info['excludewords'], match_data) != True:
                    d['sort_num'] += 1
                    if info['parent_id'] not in d['parent_id']:
                        d['parent_id'].append(info['parent_id'])
                        d['class_id'].append(info['class_id'])
        elif info['simultaneouswords'] != '' and info['excludewords'] != '':
            if contain_keywords(info['keywords'], match_data):
                if contain_keywords(info['simultaneouswords'], match_data):
                    if contain_keywords(info['excludewords'], match_data) != True:
                        d['sort_num'] += 1
                        if info['parent_id'] not in d['parent_id']:
                            d['parent_id'].append(info['parent_id'])
                            d['class_id'].append(info['class_id'])
    return d




# 主题 theam subject id


def upload_many_data(data_list, industry_name, datacenter_id, info):
    """
    多数据插入

    """
    myredis = my_redis()
    table_name = tables[industry_name]
    # 查询行业id
    sql_industry_id = "select id from TS_Industry where name='" + industry_name + "'"
    industry_id = db_b.execute_query(sql_industry_id)[0][0]

    tuple_data_list_ts_a = []
    tuple_data_list_qbb_a = []
    post_data_list_event_2_1 = []

    for work_id, data in enumerate(data_list):
        # 生成雪花id
        # print(data['链接'])
        """
        datacenter_id:页数 或者 关键字id
        work_id:第几条
        """
        worker = IdWorker(datacenter_id, work_id + 1, 0)
        id = worker.get_id()
        data['id'] = id

        post_data = {"industryNewsId": id, "tableName": table_name.split(".")[-1]}
        post_data_list_event_2_1.append(post_data)
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
    tag_data = {
        'queues': 'task.msg.event_2.1',
        'message': str(post_data_list_event_2_1)
    }
    url = 'http://localhost:8090/jms/send_array'
    proxies = {'http': None, 'https': None}
    requests.get(url=url, proxies=proxies, params=tag_data)


    # sql_ts_a_second_data = "insert into TS_Second_Data (id,industry_id,ic_id,keywords_id,url) values (%d,%d,%s,%s,%s)"
    sql_ts_a = "insert into TS_A." + table_name + " (id,industry_id,title,summary,content,url,author," \
                                                  "publish_time,emotion_status) values (%d,%d,%s,%s,%s,%s,%s,%s,%s)"
    #     schemas
    sql_qbb_a = "insert into QBB_A." + table_name + "(id,industry_id,title,summary,content,url,author,publish_time," \
                                                    "is_original,location,emotion_status) " \
                                                    "values (%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    #
    # 插入A库
    db_a.execute_many(sql_ts_a, tuple_data_list_ts_a)
    # 插入qbba库
    db_qbba.execute_many(sql_qbb_a, tuple_data_list_qbb_a)

    """
        info['id']:Customer ID
        info['xxxword']:所有检测主题XXX词
    
    """
    sql_of_Tid = "select T_Id,Word,SimultaneousWord,ExcludeWord from QBB_A.dbo.TS_Keywords where C_Id=%s group by" \
                 " T_Id,Word,SimultaneousWord,ExcludeWord" % info['id']

    thream_info_list = []

    # First check the topic ID based on the customer ID
    T_id = db_qbba.execute_query(sql_of_Tid)
    for tt in T_id:
        info_t = {
            'id': info['id'],
            'industry_name': info['industry_name'],
            'keywords': tt[1].encode('latin1').decode('gbk') if tt[1] else '',
            'excludewords': tt[-1].encode('latin1').decode('gbk') if tt[-1] else '',
            'simultaneouswords': tt[-2].encode('latin1').decode('gbk') if tt[-2] else '',
            'T_Id': tt[0],  # Monitoring subject ID
        }
        thream_info_list.append(info_t)


    print("数据量为:",len(data_list))
    for index,d in enumerate(data_list):
        d['sort_num']=0
        d['parent_id']=[]
        d['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        domain_sub=parse.urlparse(d['链接']).netloc.replace("www.","")
        rx = domain_sub.split(".")
        domain_search='.'.join(rx)
        for i in range(0, len(rx) - 1):
            if r.hexists("url", '.'.join(rx[i:])):
                ret = eval(r.hget("url", domain_search))
                d['S_Id'] = ret[-2]  # medium_type
                # source_type:TS_MediumURL 的 id 自动增长
                d['source_type'] = ret[0]
                flag = 1
                break
        # 没有domain匹配成功插入
        if flag == 0:
            # if r.hexists("url", '.'.join(rx[0:])):
            # 插入更新TS_MediumURL数据
            url_data = (domain_search, "全网", domain_search, 8, 1)
            sql_MediumSource_Type = "insert into TS_MediumURL (source_name,source_type,domain,medium_type,stat)" \
                                    " values(%s,%s,%s,%d,%d)"
            db_qbbb.execute(sql_MediumSource_Type, url_data)
            SQL_SELECT = "SELECT top 1 * FROM TS_MediumURL ORDER BY id DESC"
            URL_DATA = db_qbbb.execute_query(SQL_SELECT)[0]
            # 更新redis
            r.hset("url", domain_search, str(URL_DATA))
            # 更改数据
            d['S_Id'] = 8
            d['source_type'] = URL_DATA[0]

        # 原创转发处理
        # 当数据为微信/问答类时（S_Id=3/9）均为原创
        if d['S_Id'] == 3 or d['S_Id'] == 9:
            d['sort'] = 1
        # 微博数据
        elif d['S_Id'] == 7:
            if d['sort'] == "原创":
                d['sort'] = 1
            elif d['sort'] == "转发":
                d['sort'] = 0
        # 其他均为转发
        else:
            d['sort'] = 0
        print("第几个:",index)
        mark_java_match_data(d,thream_info_list)

    myredis.close()
    # post_mq.close_mq()

def match_insert_alone_data(data,info,T_id):
    """
    最终插入数据
    :param data:传入来的单条数据
    :param info:
    :param T_id:一级主题id
    :return:
    """

    # 只匹配了一级主题
    if data['sort_num'] == 0:
        post_data = {
            "cid": info['id'],
            "sn": data['SN'],
            # "msld": d['subject_id'],
            "msld": T_id,
            "title": data['标题'],
            "msNodeld": data['subject_id'],
            "publishDate": data['时间']
        }
        proxies = {'http': None, 'https': None}
        similar_data = {
            'queues': 'task.msg.similar_2.1',
            'message': str(post_data)
        }
        url = 'http://localhost:8090/jms/send'
        requests.get(url=url, proxies=proxies, params=similar_data)
        insert_b_data = ((data['C_Id'], data['SN'], T_id, 0, 0, 0))
        sql_DataMerger_Extend_MSubject_Map = "insert into TS_DataMerger_Extend_MSubject_Map " \
                                             "(c_id,SN,ms_id,ms_node_id,classMethod,not_first_sort) " \
                                             "values (%d,%s,%s,%s,%s,%s)"
        db_qbbb.execute(sql_DataMerger_Extend_MSubject_Map, insert_b_data)
    # 进行了1次或多次匹配
    elif data['sort_num'] >= 1:
        post_data = {
            "cid": info['id'],
            "sn": data['SN'],
            "msld": data['subject_id'],
            "title": data['标题'],
            "msNodeld": data['class_id'][0],  # 对应分类的id多分类时只发送⼀次即可，分类ID取not_first_sort=0时的数据
            "publishDate": data['时间']
        }
        proxies = {'http': None, 'https': None}
        similar_data = {
            'queues': 'task.msg.similar_2.1',
            'message': str(post_data)
        }
        url = 'http://localhost:8090/jms/send'
        requests.get(url=url, proxies=proxies, params=similar_data)
        # post_mq.send_to_queue('task.msg.similar_2.1', str(post_data))
        # 进行了一次匹配
        if len(data['class_id']) == 1:
            insert_b_data = ((data['C_Id'], data['SN'], T_id, data['class_id'][0], 0, 0))
            sql_DataMerger_Extend_MSubject_Map = "insert into TS_DataMerger_Extend_MSubject_Map " \
                                                 "(c_id,SN,ms_id,ms_node_id,classMethod,not_first_sort) " \
                                                 "values (%d,%s,%s,%s,%s,%s)"
            db_qbbb.execute(sql_DataMerger_Extend_MSubject_Map, insert_b_data)
        elif len(data['class_id']) > 1:
            for index, p in enumerate(data['class_id']):
                if (index == 0):
                    insert_b_data = ((data['C_Id'], data['SN'], T_id, p, 0, 0))
                    sql_DataMerger_Extend_MSubject_Map = "insert into TS_DataMerger_Extend_MSubject_Map " \
                                                         "(c_id,SN,ms_id,ms_node_id,classMethod,not_first_sort) " \
                                                         "values (%d,%s,%s,%s,%s,%s)"
                    db_qbbb.execute(sql_DataMerger_Extend_MSubject_Map, insert_b_data)
                else:
                    insert_b_data = ((data['C_Id'], data['SN'], T_id, p, 0, 1))
                    sql_DataMerger_Extend_MSubject_Map = "insert into TS_DataMerger_Extend_MSubject_Map " \
                                                         "(c_id,SN,ms_id,ms_node_id,classMethod,not_first_sort) " \
                                                         "values (%d,%s,%s,%s,%s,%s)"
                    db_qbbb.execute(sql_DataMerger_Extend_MSubject_Map, insert_b_data)
def mark_java_match_data(d,theam_list):
    """
    一条一条数据进行处理
    :param d:单条数据处理
    :param theam_list:主题列表
    :return:
    """
    iisql = {
        'SN': '',
        'C_Id': '',
        'S_Id': '',
        'URL': '',
        'Title': '',
        'Summary': '',
        'Body': '',
        'PublishDate_Std': '',
        'source_type': '',
        'group_SN': '',
        'like_SN': '',
        'is_original': '',
        'location': '',
        'Author_Name': '',
        'create_date': ''
    }
    match_data = d['标题'] + d['转发内容'] + d['描述']
    # 监测主题关键词进行匹配规则
    for info in theam_list:
        if match_this_theam(info,match_data):
            # 每个主题对应一个SN
            sn_id = str(uuid.uuid4())
            d['SN'] = ''.join(sn_id.split('-'))
            d['class_id'] = []
            d['sort_num']=0
            d['subject_id']=info['T_Id']
            item_dict = dict()
            item_dict.setdefault('SN', d['SN'])
            item_dict.setdefault('C_Id', d['C_Id'])
            item_dict.setdefault('S_Id', d['S_Id'])
            item_dict.setdefault('URL', d['链接'])
            item_dict.setdefault('Title', d['标题'])
            item_dict.setdefault('Summary', d['描述'])
            item_dict.setdefault('Body', d['转发内容'])
            item_dict.setdefault('PublishDate_Std', d['时间'])
            item_dict.setdefault('source_type', d['source_type'])
            item_dict.setdefault('group_SN', d['SN'])
            item_dict.setdefault('like_SN', d['SN'])
            item_dict.setdefault('is_original', d['sort'])
            item_dict.setdefault('location', d['area'])
            item_dict.setdefault('Author_Name', d['发布人'])
            item_dict.setdefault('create_date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            table_name = tables[info['industry_name']].split(".")[-1]
            post_data = {
                "id": d['id'],
                "cid": d['C_Id'],
                "sn": d['SN'],
                "emotionStatus": d['positive_prob_number'],
                "tableName": table_name
            }
            # 情感处理发送的数据
            emotion_2_data = {
                'queues': 'task.msg.emotion_2.1',
                'message': str(post_data)
            }
            url = 'http://localhost:8090/jms/send'
            # 单条
            proxies = {'http': None, 'https': None}
            requests.get(url=url, proxies=proxies, params=emotion_2_data)
            tag_data = {
                'queues': 'task.msg.tag_2.1',
                'message': str({"sN": d['SN'], "cId": d['C_Id']})
            }
            requests.get(url=url, proxies=proxies, params=tag_data)
            # 数据插入B库
            sql_of_base = 'insert into TS_DataMerge_Base ({}) values ({})'. \
                format(",".join(iisql.keys()), ",".join(['%s'] * len(iisql.keys())))
            db_qbbb.execute(sql_of_base, tuple(item_dict.values()))

            if info['keywords'] != '':
                if info['excludewords'] == '' and info['simultaneouswords'] == '':
                    if contain_keywords(info['keywords'], match_data):
                        # 下面的子类进行匹配
                        sub_class_match_data(info,d)
                        match_insert_alone_data(d,info,info['T_Id'])
                elif info['simultaneouswords'] != '' and info['excludewords'] == '':
                    if contain_keywords(info['keywords'], match_data):
                        if contain_keywords(info['simultaneouswords'], match_data):
                            sub_class_match_data(info,d)
                            match_insert_alone_data(d, info, info['T_Id'])
                elif info['simultaneouswords'] == '' and info['excludewords'] != '':
                    if contain_keywords(info['keywords'], match_data):
                        if contain_keywords(info['excludewords'], match_data) != True:
                            sub_class_match_data(info,d)
                            match_insert_alone_data(d, info, info['T_Id'])
                elif info['simultaneouswords'] != '' and info['excludewords'] != '':
                    if contain_keywords(info['keywords'], match_data):
                        if contain_keywords(info['simultaneouswords'], match_data):
                            if contain_keywords(info['excludewords'], match_data) != True:
                                sub_class_match_data(info,d)
                                match_insert_alone_data(d, info, info['T_Id'])


def match_this_theam(info,match_data):
    if info['keywords'] != '':
        if info['excludewords'] == '' and info['simultaneouswords'] == '':
            if contain_keywords(info['keywords'], match_data):
                # 下面的子类进行匹配
                return True
            else:
                return False
        elif info['simultaneouswords'] != '' and info['excludewords'] == '':
            if contain_keywords(info['keywords'], match_data):
                if contain_keywords(info['simultaneouswords'], match_data):
                    return True
                else:
                    return False
        elif info['simultaneouswords'] == '' and info['excludewords'] != '':
            if contain_keywords(info['keywords'], match_data):
                if contain_keywords(info['excludewords'], match_data) != True:
                    return True
                else:
                    return False
        elif info['simultaneouswords'] != '' and info['excludewords'] != '':
            if contain_keywords(info['keywords'], match_data):
                if contain_keywords(info['simultaneouswords'], match_data):
                    if contain_keywords(info['excludewords'], match_data) != True:
                        return True
                    else:
                        return False
def sub_class_match_data(info,d):
    """
    匹配分类
    :param info:监测主题的信息
    :param d:单条数据
    :return:
    """
    sql = "select A.id,C_Id,parent_id,subject_id,classId,ruleContent,homonymWords,exclusionWords from " \
          "QBB_B.dbo.TS_MonitorSubject as A inner join QBB_B.dbo.TS_MonitorSubject_rules as B " \
          "on A.id=B.classId where A.subject_id={0} and A.id!={0} and parent_id={0}".format(info['T_Id'])

    # 获得当前监测主题下的所有子分类
    sub_class_datas = db_qbbb.execute_query(sql)
    listdict = ['A_id', 'C_Id', 'parent_id', 'subject_id',
                'classId', 'ruleContent', 'homonymWords',
                'exclusionWords']
    # 子类进行匹配
    def match_sub_class_data(class_info,data):
        """
        子类进行匹配
        :param class_info:子类信息
        :param data:单条
        :return:
        """
        sql_sub_class = "select A.id,C_Id,parent_id,subject_id,classId,ruleContent,homonymWords,exclusionWords from " \
                  "QBB_B.dbo.TS_MonitorSubject as A inner join QBB_B.dbo.TS_MonitorSubject_rules as B " \
                  "on A.id=B.classId where A.subject_id={0} and A.id!={0} " \
                  "and parent_id={1}".format(class_info['subject_id'], class_info['A_id'])
        # 查看当前分类下面是否有子分类
        item_sub_class = db_qbbb.execute_query(sql_sub_class)

        info = dict()
        info['keywords'] = class_info['ruleContent']
        info['simultaneouswords'] = class_info['homonymWords']
        info['excludewords'] = class_info['exclusionWords']
        # 当前分类的id

        info['parent_id'] = class_info['parent_id']
        # 当前id
        info['class_id'] = class_info['A_id']

        # 是否匹配当前分类 进行处理 sort_num和parent_id
        curent_class_data = match_alone_keyword_(info, data)
        if len(curent_class_data['class_id'])!=0:
            # 获取当前级别的数据
            for i_data in item_sub_class:
                item_son_data = dict(zip(listdict, list(i_data)))
                item_son_data['ruleContent'] = item_son_data['ruleContent'].encode('latin1').decode('gbk')
                item_son_data['homonymWords'] = item_son_data['homonymWords'].encode('latin1').decode('gbk')
                item_son_data['exclusionWords'] = item_son_data['exclusionWords'].encode('latin1').decode('gbk')
                match_sub_class_data(item_son_data, curent_class_data)

    # 对子每一个二级分类进行过滤

    for item in sub_class_datas:
        i_data = dict(zip(listdict, list(item)))
        d['subject_id'] = i_data['subject_id']
        i_data['ruleContent'] = i_data['ruleContent'].encode('latin1').decode('gbk')
        i_data['homonymWords'] = i_data['homonymWords'].encode('latin1').decode('gbk')
        i_data['exclusionWords'] = i_data['exclusionWords'].encode('latin1').decode('gbk')
        match_sub_class_data(i_data, d)


def get_month_data(time1, time2, industry_name):
    """

    :param time1:开始时间
    :param time2:结束时间
    :param industry_name:行业名字
    :return:
    """
    myredis = my_redis()

    myredis.redis.flushall()
    sql = "select industry_id,url from %s where publish_time between '%s' and '%s'" % (
        tables[industry_name], time1, time2)
    datas = db_qbba.execute_query(sql)
    for d in tqdm(iterable=datas, desc="加载<%s>数据数据" % industry_name, unit='条'):
        myredis.redis.sadd(d[0], d[1])

    sql = "select * from TS_MediumURl"
    data = db_qbbb.execute_query(sql)
    for d in tqdm(iterable=data, desc="加载url数据", unit='条'):
        myredis.redis.hset("url", d[3], str(d))

    myredis.close()


# 根据url进行二次滤重
def filter_by_url(datalist, industry_name):
    """

    :param datalist: 传入的数据
    :param industry_name:行业名字
    :return:
    """
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
    db_a.execute(sql_record, data)
    my_e = my_Email()
    if data[4] != 0 and data[5] != 0:
        if (data[5] / data[4]) < 0.7:
            my_e.send_message('数据量异常', data[6])
    elif data[4] == 0 or data[5] == 0:
        my_e.send_message('数据量异常', data[6])
    today = data[2].date()
    # sql_industry_num = """
    #         if not exists (select * from record_log_industry  where industry = '{0}' and record_time='{1}')
    #                 INSERT INTO record_log_industry (industry,record_time,upload_num) VALUES ('{0}','{1}',{2})
    #             else
    #                 UPDATE record_log_industry SET upload_num=upload_num+{2}
    #
    #                WHERE industry = '{0}' and record_time='{1}'
    #         """.format(data[0], today, data[5])
    #
    # # 行业数据表每天增加
    # # print(sql_industry_num)
    # db_a.execute(sql_industry_num)

    print("Finash record")
    # pass


def customer_log():
    """
    统计项目数据量
    B库
    """
    for customer in get_industry_keywords():
        date_now = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        date_yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

        sql_qbbb = "select count(*) from TS_DataMerge_Base where C_Id='{0}' and PublishDate_Std " \
                   "between '{2}' and '{1}'".format(customer['id'], date_now, date_yesterday)
        # qbbb 库查询的数量
        today_customer_num = db_qbbb.execute_query(sql_qbbb)[0][0]
        # 记录项目的数据量
        sql_tsa_customer = "insert into record_log_customer (customer,record_time,upload_num) values(%s,%s,%s)"
        data = (customer['customer'], date_yesterday, today_customer_num)
        db_a.execute(sql_tsa_customer, data)


if __name__ == '__main__':
    # for d in merger_industry_data(get_industry_keywords()):
    #     print(d)
    #     print("***"*20)

    for data in get_industry_keywords():
        print(data)
    # c_d=get_industry_keywords()
    # mao_d=[]
    # for d in c_d:
    #     if d['industry_name']=='流通贸易':
    #         mao_d.append(d)
    # pprint(mao_d)
    # url='http://thsggzyjy.tonghua.gov.cn/jyxx/004002/004002003/004002003002/20210621/e40bfb43-1a2c-41a7-bed5-8c68429f4a53.html'
    # fi = domain.ExtractLevelDomain()
    # for i in range(3, 0, -1):
    #     flag = 0
    #     print(i)
    #     获取XX子级域名
        # domain_level = fi.parse_url_level(url, i)
        # print(domain_level)
    #     if r.hexists("url", domain_level):
    #         ret = eval(r.hget("url", domain_level))
    #         print(ret[-2])  # medium_type)
    #         # source_type:TS_MediumURL 的 id 自动增长
    #         print(ret[0])
    #         flag = 1
    #         break
    # if flag==0:
    #     print("匹配成功")