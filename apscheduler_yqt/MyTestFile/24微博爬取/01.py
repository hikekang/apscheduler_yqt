# _*_coding:utf-8 _*_
# @Time　　:2021/9/8   17:18
# @Author　 : Antipa
# @ File　　  :01.py
# @Software  :PyCharm
# @Description


# https://weibo.com/5931215633/KxdY9cCK1?type=comment

import requests
url="https://weibo.com/5931215633/KxdY9cCK1?type=comment"
heasers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",

    }
cookies={
        'login_sid_':'ebbedd2984ad1bdcad47de4d5484c696',
        '_s_tentry':'-',
        'Apache':'Apache=4936835532755.024.1631092500650',
        'SINAGLOBAL':'8598167916889.414.1493773707704',
        'ULV':'ULV=1631092500654:2:2:2:4936835532755.024.1631092500650:1631081674388',
        'SCF':'An3a20Qu9caOfsjo36dVvRQh7tKzwKwWXX7CdmypYAwRoCoWM94zrQyZ-5QJPjjDRpp2fBxA_9d6-06C8vLD490.',
        'SUB':'_2A250DV37DeThGeNO7FEX9i3IyziIHXVXe8gzrDV8PUNbmtAKLWbEkW8qBangfcJP4zc_n3aYnbcaf1aVNA..',
        'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WhR6nHCyWoXhugM0PU8VZAu5JpX5K2hUgL.Fo-7S0ecSoeXehB2dJLoI7pX9PiEIgij9gpD9J-t',
        'SUHB':'0jBY7fPNWFbwRJ',
        'UOR':',,www.baidu.com',
}
proxy={
    "http":None,
    "https":None
}
result=requests.get(url,headers=heasers,cookies=cookies,proxies=proxy)
print(result.text)

