#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/17 16:48
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 表格图片一.py
 Description:
 Software   : PyCharm
"""
# -*- coding: utf-8 -*-
import os

os.chdir(r'F:\自动化报表')  # 设置文件路径

import numpy as np
import pandas as pd

import smtplib
from email.message import EmailMessage
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Part 0 set initial parameter
mail_user = 'hikekhd'  # 邮箱登录名，此处使用QQ邮箱，填写QQ号即可，不用带@qq.com
mail_pass = 'RTWFIATJGIYXZEKT'  # QQ邮箱授权码，可百度如何获取

sender = 'hikekhd@163.com'  # 发件人
receivers = ['haidong.kang@datagalaxy.cn']  # 收件人列表，list形式
chaosong = ['haidong.kang@datagalaxy.cn']  # 抄送人列表，list形式

# 设置邮件体对象
msg = MIMEMultipart()  # 邮件体对象，此处可加入参数， 具体可百度
subject = 'python send email test'  # 邮件主题
msg['subject'] = Header(subject, 'utf-8')  # 加入邮件主题
msg['From'] = "{}".format(sender)  # 加入邮件发送人
msg['To'] = ",".join(receivers)  # 加入邮件接收人
msg['Cc'] = ",".join(chaosong)  # 加入邮件抄送人，如无，可注释掉

# Part 1 文本内容
text_content = """This is a test email"""
textApart = MIMEText(text_content, 'plain', 'utf-8')
msg.attach(textApart)

# Part 2.1 发送单个附件
pdfFile = r"F:\自动化报表\test.pdf"
pdfName = 'test.pdf'
pdfApart = MIMEApplication(open(pdfFile, 'rb').read())
pdfApart.add_header('Content-Disposition', 'attachment', filename=pdfName)
msg.attach(pdfApart)
# Part 6 发送邮件，参数设置
sftp_obj = smtplib.SMTP_SSL(host='smtp.163.com', port=25)
sftp_obj.login(mail_user, mail_pass)
sftp_obj.sendmail(sender, receivers, msg.as_string())
sftp_obj.quit()
sftp_obj.close()
print('\nThe email has been sent successfully')
del msg
# Part 2.2 发送多个附件
files = ['temp.xlsx', 'test.pdf']
for i in np.arange(len(files)):
    attFile = MIMEApplication(open(files[i], 'rb').read())
    attFile.add_header('Content-Disposition', 'attachment', filename=files[i])
    msg.attach(attFile)

# Part 3.1 网页内容，有链接，插入图片; 如果同时发送网页内容和纯文本，只保留网页内容。因不影响使用，未追查原因
htmlFile = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
    <p>图片演示：
    <br /><img src="cid:0", width=200, height=180  ></p>
  </body>
</html>
"""  # 图片演示下的 cid 后的内容（可能不是数字）需与 下面 imageApart.add_header('Content-ID', '<0>') 的<>内容一致
htmlApart = MIMEText(htmlFile, 'html')

# 在正文中显示图片
imageFile = 'trees in automn.png'
imageApart = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
imageApart.add_header('Content-ID', '<0>')
msg.attach(imageApart)
msg.attach(htmlApart)

# Part 3.2 在附件中显示图片。Part 3.1 只能在正文显示图片，如果想同时将同一张图片加入附件，可用如下代码
attachImage = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
attachImage.add_header('Content-Disposition', 'attachment', filename=imageFile)
msg.attach(attachImage)

# Part 4 在HTML或附件中显示多张图片
# 网页内容，有链接，插入多张图片
htmlFile = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
    <p>图片演示flowers：
    <br /><img src="cid:0", width=200, height=180  >
    <br />第四张图片：
    <br /><img src="cid:1", width=200, height=180  >
    <br />向阳而生的树木：
    <br /><img src="cid:2", width=200, height=180  >
    <br />秋天的树木：
    <br /><img src="cid:3", width=200, height=180  >
    </p>
  </body>
</html>
"""
htmlApart = MIMEText(htmlFile, 'html')

# 在正文中显示多张图片
images = [i for i in os.listdir() if i.endswith(('.jpg', '.png'))]  # images列表存放要发送的图片附件，路径已设置，见开头，此处未用全路径
for i in np.arange(len(images)):
    imageFile = images[i]
    imageMultiApart = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
    imageMultiApart.add_header('Content-ID', '<%i>' % i)
    msg.attach(imageMultiApart)
msg.attach(htmlApart)

# 在附件中显示多张图片， 可与 part 2.2 合并
for i in np.arange(len(images)):
    imageFile = images[i]
    attachImage = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
    attachImage.add_header('Content-Disposition', 'attachment', filename=imageFile)
    msg.attach(attachImage)

# Part 5
# 邮件正文中嵌入表格，比较简单的单行单列的表格，即同一行或同一列中没有其他合并的单元格
pd.set_option('display.max_colwidth', -1)
df = pd.read_excel('temp.xlsx', nrows=5)
# df['缩略图'] = '<img src="' + df['缩略图'] + '">' # 表中含有图片链接时的转换，如为普通数据，可注释掉
table_title = " 表格标题"


def get_html_msg(df, table_title):
    """
    1. 构造html信息
    """
    df_html = df.to_html(escape=False)

    # 表格格式
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>
                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }
                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }
                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }
                table.dataframe tr {
                }
                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }
                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }
                body {
                    font-family: 宋体;
                }
                h1 {
                    color: #5db446
                }
                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }
                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }
                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }
                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }
                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }
            </STYLE>
        </head>
        """

    # 构造正文表格
    body = \
        """
        <body>
        <div align="center" class="header">
            <!--标题部分的信息-->
            <h1 align="center">{table_title}</h1>
        </div>
        <hr>
        <div class="content">
            <!--正文内容-->
            <h2>带图片展示的表格</h2>
            <div>
                <h4></h4>
                {df_html}
            </div>
            <hr>
            <p style="text-align: center"> </p>
        </div>
        </body>
        """.format(df_html=df_html, table_title=table_title)

    html_msg = "<html>" + head + body + "</html>"
    #   这里是将HTML文件输出，作为测试的时候，查看格式用的，正式脚本中可以注释掉
    #   fout = open('test.html', 'w', encoding='UTF-8', newline='')
    #   fout.write(html_msg)
    return html_msg


# html 内容
html_msg = get_html_msg(df, table_title)
content_html = MIMEText(html_msg, "html", "utf-8")
msg.attach(content_html)

# Part 6 发送邮件，参数设置
sftp_obj = smtplib.SMTP_SSL(host='smtp.163.com', port=25)
sftp_obj.login(mail_user, mail_pass)
sftp_obj.sendmail(sender, receivers, msg.as_string())
sftp_obj.quit()
sftp_obj.close()
print('\nThe email has been sent successfully')
del msg
