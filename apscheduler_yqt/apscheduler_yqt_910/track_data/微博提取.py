# _*_coding:utf-8 _*_
# @Time　　:2021/9/16   11:41
# @Author　 : Ben
# @ File　　  :微博提取.py
# @Software  :PyCharm
# @Description
from lxml import etree

with open('html.html',"r") as file:
    html_content=file.read()

doc=etree(html_content)
li_list=doc.xpath('//ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li')
for i in range(1,4):
    li_list[i].xpath('//a/span/span/em')
print("aaa")