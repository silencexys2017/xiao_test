#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from abc_html import msg

# 设置登录及服务器信息
mail_host = "smtp.exmail.qq.com"
mail_user = "service@perfee.com"
mail_pass = "6t7BtccBR4S9"
sender = "service@perfee.com"
receivers = ["xiaoyongsheng@perfee.com"]

# 设置eamil信息
message = MIMEMultipart()  # 添加一个MIMEmultipart类，处理正文及附件
message['From'] = sender
message['To'] = ",".join(receivers)
message['Subject'] = Header("xiao test", 'utf-8')

# 推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
with open('abc_html.py', 'r', encoding="utf-8") as f:
    # content = """
    #  <p>你好，Python 邮件发送测试...</p>
    #  <p>这是使用python登录qq邮箱发送HTML格式和图片的测试邮件：</p>
    #  <p><a href='http://www.yiibai.com'>易百教程</a></p>
    #  <p>图片演示：</p>
    #  <p>![](cid:send_image)</p>
    # """
    # content = f.read()
    part1 = MIMEText(msg, 'html', 'utf-8')
    message.attach(part1)

# 添加一个xlsx文本附件
with open('clearing.xlsx', 'rb') as h:
    part2 = MIMEText(h.read(), 'base64', 'utf-8')
    # 附件设置内容类型，方便起见，设置为二进制流
    part2['Content-Type'] = 'application/octet-stream'
    part2['Content-Disposition'] = 'attachment;filename="abc.xlsx"'
    message.attach(part2)

# 添加照片附件
with open('24.jpg', 'rb')as fp:
    picture = MIMEImage(fp.read())
    picture['Content-Type'] = 'application/octet-stream'
    picture['Content-Disposition'] = 'attachment;filename="1.png"'
    message.attach(picture)


# 登录并发送邮件
try:
    smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
    smtp_obj.login(mail_user, mail_pass)
    smtp_obj.sendmail(
        sender, receivers, message.as_string())
    smtp_obj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error', e)
