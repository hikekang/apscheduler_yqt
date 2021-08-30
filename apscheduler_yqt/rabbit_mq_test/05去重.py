#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/16 11:49
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 05去重.py
 Description:对B库数据进行去重
 Software   : PyCharm
"""
from utils.ssql_pool_helper import DataBase,config_QBBB,config_QBBA_net
import datetime
db_qbbb = DataBase('sqlserver', config_QBBB)
# db_qbba_net = DataBase('sqlserver', config_QBBA_net)

def delete_Repeat(c_id,days):
    date_now=(datetime.datetime.now()).strftime('%Y-%m-%d 00:00:00')
    # 去重
    date_de_duplication=(datetime.datetime.now()-datetime.timedelta(days=days)).strftime('%Y-%m-%d 00:00:00')
    sql1=f"""
    select URL from QBB_B.dbo.TS_DataMerge_Base with (NOLOCK) where  C_Id='{c_id}'
    and PublishDate_Std between '{date_de_duplication}' and '{date_now}' group by URL having count(url)>1
    """
    chongfu_data=db_qbbb.execute_query(sql1)
    print(len(chongfu_data))
    for item in chongfu_data:
        sql2=f"""
            select SN from QBB_B.dbo.TS_DataMerge_Base with (NOLOCK) where  C_Id='{c_id}'
    and PublishDate_Std between '{date_de_duplication}' and '{date_now}' and URL='{item[0]}' order by create_date asc
        """
        cc_2=db_qbbb.execute_query(sql2)
        print(cc_2)
        # for it in cc_2:
        if cc_2:
            for i in range(len(cc_2)-1):
                # print(i)
                delete_item=cc_2[i][0]
                # print(delete_item)
                sql3=f"delete from QBB_B.dbo.TS_DataMerge_Base where SN='{delete_item}' "
                sql4=f"delete from QBB_B.dbo.TS_DataMerge_Extend where SN='{delete_item}'"
                sql5=f"delete from QBB_B.dbo.TS_DataMerger_Extend_Mark_Map where SN='{delete_item}'"
                sql6=f"delete from QBB_B.dbo.TS_DataMerger_Extend_MSubject_Map where SN='{delete_item}'"
                db_qbbb.execute(sql3)
                db_qbbb.execute(sql4)
                db_qbbb.execute(sql5)
                db_qbbb.execute(sql6)
                db_qbbb.execute(sql3)
        # print(cc_2)
        # sql3=""
def title_deal():
    sql="select SN,Author_Name from QBB_B.dbo.TS_DataMerge_Base where Author_Name like '%：%' and PublishDate_Std >'2021-08-01 12:34:14'"
    data=db_qbbb.execute_query(sql)

    for d in data:
        # print(d[1].encode('latin1').decode('gbk').split("：")[0])
        author=d[1].encode('latin1').decode('gbk').split("：")[0]
        update_sql = "update QBB_B.dbo.TS_DataMerge_Base set Author_Name='{1}' where SN='{0}'  ".format(d[0],author)
        print(update_sql)
        # print(d[1].encode('latin1').decode('gbk'))
        # print(d[1].split("："))
        db_qbbb.execute(update_sql)
        # print(d[0])
    sql = "select SN,Author_Name from QBB_B.dbo.TS_DataMerge_Base where Author_Name like '%:%' and PublishDate_Std >'2021-08-01 12:34:14'"
    data = db_qbbb.execute_query(sql)

    # for d in data:
    #     # print(d[1].encode('latin1').decode('gbk').split("：")[0])
    #     author = d[1].encode('latin1').decode('gbk').split(":")[0]
    #     update_sql = "update QBB_B.dbo.TS_DataMerge_Base set Author_Name='{1}' where SN='{0}'  ".format(d[0], author)
    #     print(update_sql)
    #     # print(d[1].encode('latin1').decode('gbk'))
    #     # print(d[1].split("："))
    #     db_qbbb.execute(update_sql)
        # print(d[0])
if __name__ == '__main__':
    # # 柯尼卡
    # delete_Repeat(1410138327104954370)
    # 优速
    # delete_Repeat(1369902503931461634)
    # 三联集团
    delete_Repeat(1410137352906547202,days=2)

    # title_deal()