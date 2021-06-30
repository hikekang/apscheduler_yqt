# -*- coding: utf-8 -*-
"""
   File Name：     测试
   Description :
   Author :       hike
   time：          2021/4/28 16:33
"""
keywords='蒙牛|伊利|完达山|君乐宝|三元牛奶|圣元|合生元|雀巢牛奶|雀巢奶粉|光明牛奶|光明酸奶|光明乳业|妙可蓝多|特仑苏|金典|白小纯|飞鹤|贝因美|现代牧业|太子乐|旺仔牛奶|惠氏|美赞臣|雅培|金领冠|雅士利|'
keywords_list=keywords.split('|')
print(keywords_list)

text='卧槽，光明的新鲜牧场即便宜又好喝//@Einsamkeit诶哟喂叉会儿老腰://@-姑苏小白-: 光明太惨了。。。//@鸠也子: 光明做错了什么要被牛皮癣沾上//@卡了蛋儿kk:yue了，居然碰瓷我最爱的新鲜牧场://@光明乳业:您的反馈我们已经收到！您反应的问题我们很重视'
for keywords in keywords_list:
    if keywords in text:
        print(keywords)


num=2
nums=[]
for i in range(0,10):
    nums.append(i)
flag=0
for i in range(10,12):
    print(i)
    for n in nums:
        print(n)
        if num==n:
            flag=1
    if flag==0:
        print("haha")