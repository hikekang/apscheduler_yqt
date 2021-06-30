#!/usr/bin/python3.x
# -*- coding: utf-8 -*-
# @Time    : 2021/5/17 17:25
# @Author  : hike
# @Email   : hikehaidong@gmail.com
# @File    : unicode编码.py
# @Software: PyCharm
# str="""content:  <font color="red">华为</font>官方已宣布将于 5 月 19 日 14:30 发布 <font color="red">华为</font> FreeBuds 4 真 无线耳机。 打开APP，¥çæ´å¤ç²¾å½©å¾çä»å®æ¹æ¾åºçæ¸²æå¾æ¥çï¼<font color="red">åä¸º</font> FreeBuds 4 è³æºååçµççæ´ä½è®¾è®¡åè·ä¸ä»£äº§å<font color="red">åä¸º</font> FreeBuds 3 ç±»ä¼¼ãææ°ç åä¸»éé²ï¼è½ç¶è¿æ¬¾è³æºå¤è§ä¸åä»£æ²¡å¤å¤§å·®å«ï¼ä½å®éä¸è¿æ¬¾äº§åçè¿­ä»£è¿æ¯æç¸å½çåçº§ãåè½è®¾è®¡ä¸ä¸»æçâèééåªâéå¸¸å¼å¾æå¾ï¼åæ¶å¨ä½©æ´çèéæ§ãé³è´¨ã<font color="red">ç»­èª</font>ç­æ¹é¢é½ææåã<font color="red">åä¸º</font> FreeBuds 4 å·²ç»å¨ <font color="red">åä¸º</font>ååå¼å¯é¢çº¦ï¼ä»é¢çº¦é¡µé¢æ¥çï¼è¯¥æºè³æºè³å°æä¾ç½è²ãç°è²åçº¢è²ä¸ç§é¢è²ãä½ä»æ­¤åçææ¥çè¿å°æ¥æé»è²ãé¶è²çæ¬ã <font color="red">åä¸º</font> FreeBuds 3 çæ çº¿è³æºåå¸äº 2019 å¹´ï¼æ­è½½éºéº A1 è¯çï¼æ¯æéª¨å£°çº¹éè¯éåªï¼æ¯å¨çé¦æ¬¾éç¨å¼æ¾å¼è®¾è®¡ãå´æ¯æ ä¸»å¨éåªççæ çº¿è³æºï¼ä¹æ¯ä¸çä¸ç¬¬ä¸æ¬¾çæ­£çèç 5.1 æ çº¿è³æºã """""
# print(str)
#
# import jieba
#
#
# def if_contain_chaos(keyword):
#     str_len = len(keyword)
#     seg_len = len(jieba.lcut(keyword))
#
#     if str_len / seg_len < 2:
#         return True
#     else:
#         return False
# print(if_contain_chaos(str))
#
# def if_contain_chaos(keyword):
#     try:
#         keyword.encode("gb2312")
#     except UnicodeEncodeError:
#         return True
#     return False
#
# print(if_contain_chaos(str))

# f_charInfo的输出是这样的的一个字典{'confidence': 0.99, 'encoding': 'utf-8'}

str='/ 50 '
str_int=int(str.split('/')[-1])
print(str_int)
str=' 非敏感 '
import re
p=re.compile("r'\s*|\t|\r|\n|&nbsp|'")
print(p.sub(" ",str))
print(str.split()[0])