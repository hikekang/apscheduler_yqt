# _*_coding:utf-8 _*_
# @Time　　:2021/9/16   11:31
# @Author　 : Ben
# @ File　　  :正则提取.py
# @Software  :PyCharm
# @Description
import re

with open("weibo_content.txt","r+") as file:
    content=file.read()

match=re.findall("<script>FM.view(.*)</script>",content)
print("aaa")