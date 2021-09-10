# _*_coding:utf-8 _*_
# @Time　　:2021/9/10   13:48
# @Author　 : Antipa
# @ File　　  :正则测试.py
# @Software  :PyCharm
# @Description
import re
pattern = re.compile(r'http://weibo.com.*')
result=re.findall(pattern,"http://weibo.com/6107880472/KcBjyBn8Y")
print(result)
