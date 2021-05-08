# -*- coding: utf-8 -*-
"""
   File Name：     email_helper
   Description :
   Author :       hike
   time：          2021/5/8 13:47
"""
import smtplib
from email.mime.text import MIMEText
class my_Email():
    def __init__(self):
        # 设置服务器所需信息
        # 163邮箱服务器地址
        self.mail_host = 'smtp.163.com'
        # 163用户名
        self.mail_user = 'hikekhd'
        # 密码(部分邮箱为授权码)
        self.mail_pass = 'RTWFIATJGIYXZEKT'
        # 邮件发送方邮箱地址
        self.sender = 'hikekhd@163.com'
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        self.receivers = ['haidong.kang@datagalaxy.cn']

    def send_message(self,content):
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '测试'
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = self.receivers[0]
        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            #连接到服务器
            smtpObj.connect(self.mail_host,25)
            #登录到服务器
            smtpObj.login(self.mail_user,self.mail_pass)
            #发送
            smtpObj.sendmail(self.sender,self.receivers,message.as_string())
            #退出
            smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error',e) #打印错误