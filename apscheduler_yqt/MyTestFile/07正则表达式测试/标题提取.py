#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/9 10:20
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 标题提取.py
 Description:
 Software   : PyCharm
"""
content="""

<pre style="white-space: pre-wrap;white-space: -moz-pre-wrap;white-space: -pre-wrap;white-space: -o-pre-wrap; word-wrap: break-word;"><zhengwen>@菜籽油反黑组 #蔡徐坤[超话]#?? #蔡徐坤新专辑迷上线#  210804-2   14:01 打卡目标：4000 【yhxx-其他】 1   （ID 小坤坤很困困 xhpp） 【yhxx-暴/恐】 ?1  举报打卡需要大家持之以恒的坚持，用行动改变现状，加油！ ??举报后请随手转发扩散并@ 三位好友 查看举报结果?? 个人评论检查??   ?[蔡徐坤松下Beauty]??[蔡徐坤燕京啤酒]??[百事可乐代言人蔡徐坤]??[戴比尔斯蔡徐坤]??[蔡徐坤屈臣氏品牌代言人]??[蔡徐坤代言康师傅喝开水]?[蔡徐坤代言惠普电脑]?[施华蔻品牌代言人蔡徐坤]?[蔡徐坤FILA]?[纪梵希彩妆代言人蔡徐坤]?[SUNCUT全球代言人蔡徐坤]?[蔡徐坤Prada代言人]</zhengwen></pre>
"""
import re
pattern=re.compile('<zhengwen>(.*)</zhengwen>')
result=pattern.findall(content)
# print(len(result))
# print(result)
title='安徽省万帮广告有限公司:【商铺信息】2021-8-9日最新商铺动态 '
title='上汽大众哈尔滨金田安达4S店:hike：【七夕礼遇 众多惊喜】8.14上汽大众约惠七夕购车节'
title_pattern=re.compile('(.*)[:|：](.*)')
title_match=title_pattern.findall(title)
# title_match=title_pattern.match(title)
print(title_match)
print(title_match[0])
print(title_match[0][0])
print(len(title_match)>=2)

#

def py_str_title(author_or_title):
    result_a_t = author_or_title.split(":")
    result_a_t_1 = author_or_title.split("：")

    if len(result_a_t) >= 2:
        author = result_a_t[0]
        title = ''.join(result_a_t[1:])
    elif len(result_a_t_1) >= 2:
        author = result_a_t_1[0]
        title = ''.join(result_a_t_1[1:])
    else:
        author = ''
        if result_a_t_1:
            title = result_a_t_1[0]
        if result_a_t:
            title = result_a_t[0]
    print("作者:%s\n标题:%s"%(author,title))
t2='上汽大众哈尔滨金田安达4S店:【七夕礼遇 众多惊喜】8.14上汽大众约惠七夕购车节'
title='上汽大众哈尔滨金田安达4S店:【七夕礼遇 众多惊喜】8.14上汽大众约惠七夕购车节：hike'
py_str_title(t2)
title3='       #壹米大薯条 #奶茶 #小吃加盟店排行榜前十名  价格跟蜜雪冰城差不多，但是口味比蜜雪冰城好喝😄加盟商来总部'
print(re.sub('\s+',"",title3))

title4='明星向前冲:艺人服务 | 模卡10元 | 见组资料·艺人PPT资料制作15元/页'
title4='闫小坏儿6:阿富汗塔利班发言人：在这个国家我们是人民的公仆，一切为人民'
title4='宋清辉：hike：影视行业正面临无比残酷的考验 或将加速行业洗牌'
# title4='王艺瑾：36氪独家'
py_str_title(title4)
# result4=title_pattern.findall(title4)
# print(result4)
# print(re.sub('\s+',"",title4))
