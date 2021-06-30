# -*- coding: utf-8 -*-
"""
   File Name：     01
   Description :
   Author :       hike
   time：          2021/5/8 13:22
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
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

    def send_message_text(self,content):
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
    def sen_message_xlsx(self):
        # 设置eamil信息
        # 添加一个MIMEmultipart类，处理正文及附件
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receivers[0]
        message['Subject'] = 'title'
        # 推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
        with open('abc.html', 'r') as f:
            content = f.read()
        # 设置html格式参数
        part1 = MIMEText(content, 'html', 'utf-8')
        # 添加一个txt文本附件
        with open('abc.txt', 'r')as h:
            content2 = h.read()
        # 设置txt参数
        part2 = MIMEText(content2, 'plain', 'utf-8')
        # 附件设置内容类型，方便起见，设置为二进制流
        part2['Content-Type'] = 'application/octet-stream'
        # 设置附件头，添加文件名
        part2['Content-Disposition'] = 'attachment;filename="abc.txt"'
        # 添加照片附件
        with open('1.png', 'rb')as fp:
            picture = MIMEImage(fp.read())
            # 与txt文件设置相似
            picture['Content-Type'] = 'application/octet-stream'
            picture['Content-Disposition'] = 'attachment;filename="1.png"'
        # 将内容附加到邮件主体中
        message.attach(part1)
        message.attach(part2)
        message.attach(picture)

        # 登录并发送
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print('success')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('error', e)

    def send_xlsx(self):
        file_name='temp.xlsx'
        attFile = MIMEApplication(open(file_name, 'rb').read())
        attFile.add_header('Content-Disposition', 'attachment', filename=file_name)
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receivers[0]
        message['Subject'] = 'title'
        message.attach(attFile)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print('success')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('error', e)

if __name__ == '__main__':
    test=my_Email()
    test.send_xlsx()
