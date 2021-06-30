# -*- coding: utf-8 -*-
"""
   File Name：     行业关键词合并
   Description :
   Author :       hike
   time：          2021/4/25 11:57
"""
list_msg=[
  {
    "id": 1369902503931461634,
    "customer": "优速",
    "industry_name": "流通贸易",
    "keywords": "壹米滴答|壹米|壹米滴答物流|优速快递|优速物流|优速|杨兴运|",
    "excludewords": "",
    "simultaneouswords": ""
  },
  {
    "id": 1382958958897008641,
    "customer": "罗马仕",
    "industry_name": "IT业",
    "keywords": "罗马仕|ROMOSS|",
    "excludewords": "",
    "simultaneouswords": ""
  },
  {
    "id": 1385066326720049154,
    "customer": "新能源汽车",
    "industry_name": "汽车业",
    "keywords": "恒驰|理想汽车|理想one|荣威|特斯拉|蔚来|五菱宏光mini|MINIEV|mini EV|宏光mini|小鹏|新能源汽车|电动汽车|威马|华为汽车|HiCar|比亚迪|欧拉|芝麻e30|",
    "excludewords": "",
    "simultaneouswords": ""
  },
  {
    "id": 1385070909349490689,
    "customer": "精酿啤酒",
    "industry_name": "快消品",
    "keywords": "精酿啤酒|白啤|黄啤|黑啤|雪花啤酒|青岛啤酒|哈啤|哈尔滨啤酒|燕京U8|原浆啤酒|自酿啤酒|手工啤酒|果味啤酒|精酿工坊|啤酒屋|啤酒坊|鲜酿啤酒|鲜啤|啤酒|泰山原浆|优布劳|",
    "excludewords": "",
    "simultaneouswords": ""
  },
  {
    "id": 1385500950201982977,
    "customer": "乳制品监测",
    "industry_name": "快消品",
    "keywords": "蒙牛|伊利|完达山|君乐宝|三元牛奶|圣元|合生元|雀巢牛奶|雀巢奶粉|光明牛奶|光明酸奶|光明乳业|妙可蓝多|特仑苏|金典|白小纯|飞鹤|贝因美|现代牧业|太子乐|旺仔牛奶|惠氏|美赞臣|雅培|金领冠|雅士利|",
    "excludewords": "",
    "simultaneouswords": ""
  }
]
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
n_d=[]
for name in set_mark:
    print(list_name_template + name + ':', end='\t')  # 打印自动创建的变量名称，采用tab分隔
    # exec('print(' + list_name_template + name + ')')  # 打印变量内容（列表）
    exec('n_d.append(' + list_name_template + name + ')')  # 打印变量内容（列表）

for d in n_d:
  for ds in d:
    print(ds)

# # print(data_list[3].update(data_list[4]))
# import pandas as pd
# pd.set_option('display.max_colwidth',1000)
# pd.set_option('display.max_columns',1000)
# pd.set_option('display.width',1000)
# df=pd.DataFrame(data_list)
# data_new=df.set_index(['industry_name','id'])
# # print(data_new)
# for d in data_new.itertuples():
#     # print(type(d))
#     print(d)
