'''
author: Rouzip
data:2017.4.x
'''

import socket
import re
from concurrent.futures import ThreadPoolExecutor
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import pymysql


'''
重构思路：
1.通信协议需要进行改变，由于注册功能的添加，用户可能提交的是注册，也可能是登录
2.数据库的添加，需要对其进行封装，但是服务端维护connect
'''


class serverChat():
    # 初始化服务器，建立客户列表

    def __init__(self, user, password):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', 5000))
        self.socket.listen(100)
        self.dbconn = pymysql.connect(host='127.0.0.1',
                                      user=user,
                                      password=password,
                                      db='mysql',
                                      charset='utf8')
        # 线程池，并行处理信息
        self.threads = ThreadPoolExecutor(max_workers=100)
        # 线程表，添加用户及其地址
        self.clientList = {}

    # 服务器循环等待客户上线
    # 使用多线程tcp连接
    def serverRun(self):
        while True:
            try:
                sock, addr = self.socket.accept()
                self.threads.submit(self.recMsg, sock)
            except Exception as e:
                logging.exception(e)

    # 收到客户下线，关闭socket连接，将其从列表中删除
    def cilentQuit(self, cilentName):
        self.clientList[cilentName].close()
        for name, socket in self.clientList.items():
            socket.send(bytes(cilentName + ' has left!', encoding='utf-8'))
        self.clientList.pop(cilentName)

    # 处理消息
    '''
    改进:需要分成两个函数，一个连接注册函数进行处理，一个进行聊天处理
    '''

    def recMsg(self, socket):

        def signup():
            try:
                originTextByte = socket.recv(1024)
                text = str(originTextByte, encoding='utf-8')
                recvList = str(text).split(' ')
                name, email, password = recvList[0], recvList[1], recvList[2]
                cursor = self.dbconn.cursor()
                cursor.execute('use test')
                cursor.execute(
                    'select * from User where name=%s', name
                )
                dataInDb = cursor.fetchall()
                # 判断是否可以注册，并发送成功邮件，数据记录进入数据库
                '''
                测试，需要测试注册成功与失败
                '''
                if len(dataInDb) > 0:
                    # 数据已存在，发送标志失败0
                    socket.send(bytes('失败', encoding='utf-8'))
                    print('发送成功')
                    print('注册失败')
                    return
                else:
                    # 数据不存在，发送成功标志1
                    print('注册成功')
                    socket.send(bytes('成功', encoding='utf-8'))
                cursor.execute('insert into User values(%s,%s,%s)',
                               (name, email, password))
                self.dbconn.commit()
                # self.sendEmail(email)
                cursor.close()
                return
            except Exception as e:
                logging.exception(e)

        def login():
            try:
                loginInfo = str(msgType).split(' ')
                clientName, password = loginInfo[0], loginInfo[1]
                cursor = self.dbconn.cursor()
                cursor.execute('use test')
                cursor.execute('select name,password from User where name=%s',
                               clientName)
                dataInDb = cursor.fetchall()

                cursor.close()
                '''
                失败的几种可能，一种是没有该用户,一种是密码不对，一种是此用户已经登录
                分别发送失败1,2,3
                '''


                if not len(dataInDb):
                    socket.send(bytes('失败１', encoding='utf-8'))
                    return

                passwordInDb = dataInDb[0][1]
                print(password)
                print(passwordInDb)
                if password != passwordInDb:
                    socket.send(bytes('失败２', encoding='utf-8'))
                    return

                if clientName in self.clientList:
                    socket.send(bytes('失败３', encoding='utf-8'))
                    return

                print('成功过检测')
                socket.send(bytes('成功', encoding='utf-8'))
                print('进入聊天模式')
                return clientName


            except Exception as e:
                logging.exception(e)
        # 加入默认测试对象a，以后使用
        def chat(clientName='a'):
            try:
                # 服务器将在线的人员维护在字典之中，方便转发消息
                self.clientList[clientName] = socket
                while True:
                    messageByte = socket.recv(1024)
                    message = str(messageByte, encoding='utf-8')
                    if message == 'quit':
                        self.cilentQuit(clientName)
                        return
                    search = re.search(re.compile(r'(.*):(.*)'), message)
                    if search == None:
                        socket.send(bytes('消息格式错误', encoding='utf-8'))
                        continue
                    name = search.group(1)
                    message = search.group(2)
                    if name not in self.clientList:
                        socket.send(bytes('此人未登录', encoding='utf-8'))
                        continue
                    elif name == 'all':
                        self.sendMessageAll(clientName, message)
                    else:
                        self.sendMessagePrivate(clientName, name, message)
                else:
                    return
            except Exception as e:
                logging.exception(e)

        while True:
            # 获取处理消息类型
            msgType = str(socket.recv(1024), encoding='utf-8')
            if msgType == '注册':
                signup()
            else:
                # name = login()
                # if not name:
                #     continue
                # else:
                #     chat()
                chat()


    # 向客户端报错
    # 出错的原因一个是因为格式不对或者已经被使用，一个是聊天的时候目标不在list中
    def sendError(self, clientSocket, num):
        try:
            if num == 0:
                # 注册失败
                clientSocket.send(bytes(0))
            elif num == 1:
                # 数据库中无此人
                clientSocket.send(bytes(1))
            else:
                # 登录字典已有此人
                clientSocket.send(bytes(2))
        except Exception as e:
            logging.exception(e)

    # 发送全体信息
    def sendMessageAll(self, clientName, message):
        # 在名字中排除不需要发送的‘自己’，其他的发送消息
        messageDestination = list(self.clientList.keys())
        for name in messageDestination:
            if clientName != name:
                try:
                    self.clientList[name].send(bytes(clientName+': '+message,
                                                     encoding='utf-8'))
                except Exception as e:
                    logging.exception(e)
            else:
                continue

    # 发送私人信息
    # 需要发送的线程从服务器开始发送，发送者的名字加在发送消息的名字位置
    # 从字典之中找到需要发送的客户名字，从字典中找到socket，然后发送消息
    def sendMessagePrivate(self, clientName, name, message):
        try:
            self.clientList[name].send(bytes(name + ': ' + message,
                                             encoding='utf-8'))
            self.clientList[clientName].send(bytes('me: ' + message,
                                                   encoding='utf-8'))
        except Exception as e:
            logging.exception(e)

    #　根据client的邮件地址发送邮件

    def sendEmail(self, desAddr):
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
            desAddr = desAddr
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

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.dbconn.close()


if __name__ == '__main__':
    user = 'root'  # input('your db user name:')
    password = 'vtzf2123+'  # input('your db password:')
    with serverChat(user=user, password=password) as server:
        server.serverRun()
