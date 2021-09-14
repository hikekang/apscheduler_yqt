# _*_coding:utf-8 _*_
# @Time　　:2021/9/13   17:37
# @Author　 : Antipa
# @ File　　  :test.py
# @Software  :PyCharm
# @Description
import pika

import datetime
from utils.ssql_pool_helper import DataBase,config_myQBB_A_net
from utils import qinbaobing_ssql
db=DataBase('sqlserver',config_myQBB_A_net)

sql="""
select  publish_time,title,summary,url,content,author,location,is_original from myQBB_A.dbo.TS_industry_news_automotive
where publish_time between '2021-08-31 23:20:14' and '2021-09-01 00:01:00'
order by publish_time desc
"""

data_list=db.execute_query(sql)[290:320]

# data.encode('latin-1').decode('gbk')
# data = {
#             '时间': item['publishedMinute'],
#             '标题': ex(item['title']) if item['title'] != None else item['title'],
#             '描述': ex(item['summary']) if item['summary'] != None else item['summary'],  # 微博原创
#             '链接': item['webpageUrl'],
#             '转发内容': '',
#             '发布人': item.get('author'),
#             'comments_count': 0,
#             'sort': '转发' if int(item['repostsFlg']) == 1 else '原创',
#             'related_words': item['referenceKeyword'],
#             'site_name': item['captureWebsiteName'],
#             'area': item['province'],
#             'C_Id': info_id  # 客户id
#         }

# 清洗数据

# datetime.datetime.strptime()

clean_data_list=[]
for item in data_list:
    # print(type(item[0]))
    data = {
        '时间': item[0].strftime("%Y-%m-%d %H:%M:%S"),
        '标题': item[1].encode('latin-1').decode('gbk'),
        '描述': item[2].encode('latin-1').decode('gbk'),  # 微博原创
        '链接': item[3],
        '转发内容': item[4].encode('latin-1').decode('gbk'),
        '发布人': "伪造",
        'comments_count': 0,
        'sort': '原创',
        'related_words': '奔驰',
        'site_name': '',
        'area': item[6].encode('latin-1').decode('gbk'),
        'C_Id': "1431292190277017601",  # 客户id,
        'is_original':"1",
        'positive_prob_number':'0.1'
    }
    clean_data_list.append(data)
    print(data)

info = {'id': 1418146574617800706, 'customer': '奔驰汽车', 'industry_name': '汽车业',
        'keywords': '奔驰|利之星|smart|Benz|AMG|Mercedes|梅赛德斯', 'excludewords': '奔驰的列车|路线奔驰|杀马特', 'simultaneouswords': '',
        'email': '1@qq.com', 'yqt_keywords': '((奔驰|利之星|smart|Benz|AMG|Mercedes|梅赛德斯))', 'project_words': [
        {'keywords': '((奔驰|利之星|smart|Benz|AMG|Mercedes|梅赛德斯))', 'simultaneouswords': '',
         'excludewords': '奔驰的列车|路线奔驰|杀马特|'}]}

qinbaobing_ssql.upload_many_data(clean_data_list,info['industry_name'],5,info)


