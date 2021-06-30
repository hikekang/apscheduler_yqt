# -*- coding: utf-8 -*-
"""
   File Name：     str分词
   Description :
   Author :       hike
   time：          2021/4/16 13:12
"""
import re
# str='"{"sn":"19259aa889af41559cf54a4540c66f99","url":"https://weibo.com/ttarticle/p/show?id=2309404626242803728709"}"'
# pattern=re.compile(r'http[s]?://(?:[a-zA-Z],[0-9],[$-_@.&+],[!*\(\),],(?:%[0-9a-fA-F][0-9a-fA-F]))+')
# s=re.findall(pattern,str)
# print(s)
# s2='{"sn":"19259aa889af41559cf54a4540c66f99","url":"https://weibo.com/ttarticle/p/show?id=2309404626242803728709"}'
# print(s2.split('"')[3])
# print(eval(s2))
import jieba
# str='精酿啤酒,白啤,黄啤,黑啤,雪花啤酒,青岛啤酒,哈啤,哈尔滨啤酒,燕京U8,原浆啤酒,自酿啤酒,手工啤酒,果味啤酒,精酿工坊,啤酒屋,啤酒坊,鲜酿啤酒,鲜啤,啤酒,泰山原浆,优布劳,蒙牛,伊利,完达山,君乐宝,三元牛奶,圣元,合生元,雀巢牛奶,雀巢奶粉,光明牛奶,光明酸奶,光明乳业,妙可蓝多,特仑苏,金典,白小纯,飞鹤,贝因美,现代牧业,太子乐,旺仔牛奶,惠氏,美赞臣,雅培,金领冠,雅士利,'
str='恒驰|理想汽车|理想one|荣威|特斯拉|蔚来|五菱宏光mini|MINIEV|mini EV|宏光mini|小鹏|新能源汽车|电动汽车|威马|华为汽车|HiCar|比亚迪|欧拉|芝麻e30|'
# str_list=str.split(",")
# print(str_list)
# print(str)
# words = str.split(",")
# print (",".join(sorted(set(words), key=words.index)))
counts={}
# w=jieba.cut(str,cut_all=True)
w=jieba.cut(str)

for ww in w:
    if len(ww)==1:
        continue
    else:
        counts[ww]=counts.get(ww,0)+1

items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
print(items)
# for i in range(50):
#     w,c=items[i]
#     print("{0:<10}{1:15}".format(w,c))
