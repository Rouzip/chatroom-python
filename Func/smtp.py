import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging


def sendEmail(desAddr):
    def makeEmail():
        email = MIMEMultipart('alternative')
        message = MIMEText('您已经注册成功', 'plain', 'utf-8')
        email.attach(message)
        html = MIMEText(
            '''<html>
                <head>
                <meta charset="utf-8">
                <title>注册成功！</title>
                </head>
                <body>
                <div id="wmd-preview" class="wmd-preview"><div class="md-section-divider"></div><div class="md-section-divider"></div><h1 data-anchor-id="2x59" id="注册成功">注册成功！</h1><hr><p data-anchor-id="q0ry">恭喜您，成为Rouzip聊天室的用户！ <br>
                该程序的源代码发布在 <a href="https://github.com/Rouzip/chatroom-python" target="_blank">Rouzip的github</a> <br>
                <img src="https://gss0.baidu.com/94o3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/d439b6003af33a8759ff9e8bc45c10385243b595.jpg" alt="concat" title=""></p></div>
                </body>
               </html>'''
            '</body></html>', 'html', 'utf-8')
        email.attach(html)
        return email

    try:
        # 构建发送信息
        message = makeEmail()
        message['From'] = 'Rouzip聊天室管理员'
        message['To'] = desAddr
        message['Subject'] = '注册通知邮件'

        # 构建发送地址与具体实现发送
        fromAddr = 'rouzipking@gmail.com'
        password = 'wevewwssrlrhetku'
        desAddr = '2503431279@qq.com'
        smtpServer = 'smtp.gmail.com'
        server = smtplib.SMTP(smtpServer, 587)
        server.ehlo()
        server.starttls()
        server.set_debuglevel(1)
        server.login(fromAddr, password)
        server.sendmail(fromAddr, [desAddr], message.as_string())
        server.quit()
    except Exception as e:
        logging.exception(e)
        print('邮件发送失败！')

# 测试代码
if __name__ == '__main__':
    test = sendEmail('2503431279@qq.com')
