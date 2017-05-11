'''
author: Rouzip
data:2017.4.x
'''

import socket
import re
from concurrent.futures import ThreadPoolExecutor
import logging



class serverChat():
    # 初始化服务器，建立客户列表
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1',5000))
        self.socket.listen(100)
        self.threads = ThreadPoolExecutor(max_workers = 100)    # 线程池，并行处理信息
        self.cilentList = {}    # 线程表，添加用户及其地址


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
    def cilentQuit(self,cilentName):
        self.cilentList[cilentName].close()
        for name, socket in self.cilentList.items():
            socket.send(bytes(cilentName + ' has left!', encoding = 'utf-8'))
        self.cilentList.pop(cilentName)


    # 处理消息
    def recMsg(self, socket):
        cilentName = str(socket.recv(1024), encoding = 'utf-8')
        if cilentName == '\n':
            # 第一处报错处理，未填写用户名字
            self.sendError(socket, 1)
            socket.send(bytes('请重新登录！', encoding = 'utf-8'))
            socket.close()
        # 第二处错误处理，用户名已使用
        if cilentName in self.cilentList:
            self.sendError(socket, 2)
            socket.send(bytes('请重新登录！', encoding = 'utf-8'))
            socket.close()
        self.cilentList[cilentName] = socket
        self.sendError(self.cilentList[cilentName], 3)
        print(1)
        while True:
            messageByte = socket.recv(1024)
            message = str(messageByte, encoding = 'utf-8')

            if message == 'quit':
                self.cilentQuit(cilentName)
            search = re.search(re.compile(r'(.*):(.*)'), message)
            if search == None:
                self.sendError(socket, 3)
            name = search.group(1)
            message = search.group(2)
            if name not in self.cilentList:
                self.sendError(socket, 4)
            elif name == 'all':
                self.sendMessageAll(cilentName, message)
            else:
                self.sendMessagePrivate(cilentName, name, message)
            print(3)


    # 向客户端报错
    # 出错的原因一个是因为格式不对或者已经被使用，一个是聊天的时候目标不在list中
    def sendError(self,cilentSocket, num):
        if num == 1:
            cilentSocket.send(bytes('Error1: you should input your name!',
                                    encoding = 'utf-8'))
        elif num == 2:
            cilentSocket.send(bytes('Error2: your name has been used,please change!',
                                    encoding = 'utf-8'))
        elif num == 3:
            cilentSocket.send(bytes('Error3: your format is wrong!'))
        elif num == 4:
            cilentSocket.send(bytes('Error4: this cilent has not logged!',
                                    encoding = 'utf-8'))

    # 发送全体信息
    def sendMessageAll(self, cilentName, message):
        # 在名字中排除不需要发送的‘自己’，其他的发送消息
        messageDestination = list(self.cilentList.keys())
        for name in messageDestination:
            if cilentName != name:
                self.cilentList[name].send(bytes(cilentName + ': ' + message,
                                                 encoding = 'utf-8'))
            else:
                continue


    # 发送私人信息
    # 需要发送的线程从服务器开始发送，发送者的名字加在发送消息的名字位置
    # 从字典之中找到需要发送的客户名字，从字典中找到socket，然后发送消息
    def sendMessagePrivate(self, cilentName, name, message):
        self.cilentName[name].send(bytes(name + ': ' + message,
                                         encoding = 'utf-8'))
        print(4)
        self.cilentName[cilentName].send(bytes('me: ' + message,
                                               encoding = 'utf-8'))
        print(2)

    # 现在的想法是，单独开一个线程处理消息，一开始处理名字，添加列表，之后
    # while True循环接受信息，开启转发模式


if __name__ == '__main__':
    server = serverChat()
    server.serverRun()
