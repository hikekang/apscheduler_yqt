# _*_coding:utf-8 _*_
# @Time　　:2021/9/14   15:38
# @Author　 : Antipa
# @ File　　  :01ddddocr.py
# @Software  :PyCharm
# @Description
import ddddocr
ocr=ddddocr.DdddOcr()
with open('../验证码识别/yqt.png', 'rb') as f:
    img_bytes=f.read()

res=ocr.classification(img_bytes)
print(res)