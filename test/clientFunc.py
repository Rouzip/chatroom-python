# -*- coding: UTF-8 -*- 
'''
author: Rouzip
data:2017.4.x
'''

import logging
import socket
import time
from threading import Thread

# 服务器地址和端口由预先给定
# 服务器地址和端口由预先给定
HOST = ('127.0.0.1', 5000)


class clientChat():
    # 初始化客户端

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(HOST)
        self._name = None

    # 通过GUI初始化客户名字
    def initName(self, name):
        self._name = name

    # 向服务器发送自己的名字
    def sendName(self):
        self._socket.send(bytes(self.name, encoding='utf-8'))
        time.sleep(1)

    # 向服务器发送消息
    def sendMessage(self, message):
        messageBytes = bytes(message, encoding='utf-8')
        self._socket.send(messageBytes)

    def recvMsg(self)->bytes:
        message = self._socket.recv(1024)
        print(message)
        return message

    # 聊天时死循环接受服务器发送的消息
    def recvMessage(self):
        while True:
            # 接受1024的数据
            messageBytes = self._socket.recv(1024)
            message = str(messageBytes, encoding='utf-8')
            '''
            改为在gui输出
            '''
            print(message)


