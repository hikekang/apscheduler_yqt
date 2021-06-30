#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/17 16:44
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 表格图片.py
 Description:
 Software   : PyCharm
"""

import os

os.chdir(r'F:\自动化报表\python_excel')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['Times New Roman Uni']
mpl.rcParams['font.serif'] = ['Times New Roman Uni']
mpl.rcParams['axes.unicode_minus'] = False

import smtplib
from email.message import EmailMessage
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 显示所有内容
pd.set_option('max_colwidth', 100)


# %% 发送邮件
def send_email():
    mail_user = 'hikekhd'  # 邮箱登录名，次处使用QQ邮箱，填写QQ号即可，不用带@qq.com
    mail_pass = 'RTWFIATJGIYXZEKT'  # QQ邮箱授权码，可百度如何获取

    sender = 'hikekhd@163.com'  # 发件人
    receivers = ['haidong.kang@datagalaxy.cn']  # 收件人列表，list形式
    chaosong = ['haidong.kang@datagalaxy.cn']  # 抄送人列表，list形式

    # 设置邮件体对象，对象类型为 mixed，可以发送附件
    subject = """使用Python发送自动化报表"""  # 邮件主题
    msg = MIMEMultipart()  # 邮件体对象，此处可加入参数， 具体可百度
    msg['subject'] = Header(subject, 'utf-8')  # 加入邮件主题
    msg['From'] = "{}".format(sender)  # 加入邮件发送人
    msg['To'] = ",".join(receivers)  # 加入邮件接收人
    msg['Cc'] = ",".join(chaosong)  # 加入邮件抄送人，如无，可注释掉

    # 加入图片
    htmlFile = """\
    <html>
      <head></head>
      <body>
        <pre style="font-family:arial; margin: left;">
        Dears,
           以下是某销售产品的每日统计数据，请查收.详细数据见附件
        表1 各地线上及线下销售总额（亿元）：
        <img src="cid:0" >
        </pre>
      </body>
    </html>
    """
    htmlApart = MIMEText(htmlFile, 'html')

    # 在正文中显示图片
    File1 = 'data_image.png'  # 如果是定时发送的报表，此处可以写死
    imageApart = MIMEImage(open(File1, 'rb').read(), File1.split('.')[-1])
    imageApart.add_header('Content-ID', '<0>')
    msg.attach(imageApart)
    msg.attach(htmlApart)

    # 加入附件
    File2 = '每日统计透视表.xlsx'  # 如果是定时发送的报表，此处可以写死
    attFile = MIMEApplication(open(File2, 'rb').read())
    attFile.add_header('Content-Disposition', 'attachment', filename=File2)
    msg.attach(attFile)

    if __name__ == '__main__':
        try:
            # 发送邮件，参数设置
            sftp_obj = smtplib.SMTP_SSL(host='smtp.qq.com', port=465)
            sftp_obj.login(mail_user, mail_pass)
            sftp_obj.sendmail(sender, receivers, msg.as_string())
            sftp_obj.quit()
            sftp_obj.close()
            print('\nThe email has been sent successfully')
        except Exception as err:
            print('\n Email failed to be sent out. Please check !')
            print(err)


# %% 设置表格样式
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='black',
                     bbox=[0, 0, 1, 1], header_columns=0, ax=None,
                     cell_width=None, **kwargs):
    data_shape = data.shape

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, cellLoc='center', **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    mpl_table.set_gid('-')

    for k, cell in mpl_table._cells.items():
        if cell_width is None:
            pass
        else:
            cell.set_width(cell_width[k[1]])
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns or k[0] == data_shape[0]:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    fig.savefig('data_image.png', bbox_inches='tight')
    #    plt.show()
    return ax


# %%
# 数据处理
# 1、 修改原数据后再次发送查看邮件透视表，为了进行测试，修改了透视表源数据
df = pd.read_csv('5000 Sales Records.csv')
df['Total Revenue'] = 5
df.to_excel('sales_data.xlsx', sheet_name='5000 Sales Records', index=False)

# 2、透视表：如果不在正文中显示透视表内容，只是将透视表作为附件发送，则无需加入本部分的代码，只用1、3、4部分即可
df_pivot = df.groupby('Region', as_index=False)['Order Priority', 'Total Revenue', 'Total Cost', 'Total Profit']. \
    agg({'Order Priority': len, 'Total Revenue': sum, 'Total Cost': sum, 'Total Profit': sum})
sum_all = dict(zip(list(df_pivot.columns), ['总计'] + list(df_pivot.iloc[:, 1:].sum())))
df_pivot = df_pivot.append([sum_all], ignore_index=True)
df_pivot.iloc[:, 2:] = df_pivot.iloc[:, 2:].applymap(lambda x: str("{:.2f}".format(x)))

# 3、读取透视表数据，此时python读取的透视表数据并没有更新。
# 在透视表中透视表选项中勾选【打开时更新数据】，那么在邮件中打开透视表时，可以发现透视表更新了
dfp = pd.read_excel('每日统计透视表.xlsx')  # 透视表源表为 sales_data.xlsx
dfp.iloc[:, 2:] = dfp.iloc[:, 2:].applymap(lambda x: str("{:.2f}".format(x)))  # 处理显示小数位数

# 4、发送邮件
render_mpl_table(df_pivot, header_columns=0, col_width=3, cell_width=[0.20, 0.10, 0.10, 0.10, 0.10])
send_email()