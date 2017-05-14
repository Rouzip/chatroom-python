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
            '<html><body><h4>您已经注册成功</h4>'
            '</body></html>'	    	, 'html', 'utf-8')
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

# 测试代码
if __name__ == '__main__':
    test = sendEmail('2503431279@qq.com')
