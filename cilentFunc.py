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
HOST = ('127.0.0.1',5000)


class cilentChat():
    # 初始化客户端
    def __init__(self,name):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(HOST)
        self.name = name


    # 向服务器发送自己的名字
    def sendName(self):
        self.socket.send(bytes(self.name, encoding = 'utf-8'))
        time.sleep(1)


    # 向服务器发送消息
    def sendMessage(self):
        while True:
            # message = input('<<')
            message = 'lilian:aa'
            print(message)
            messageBytes = bytes(message, encoding = 'utf-8')
            self.socket.send(messageBytes)
            time.sleep(10)


    # 接受服务器发送的消息
    def recvMessage(self):
        while True:
        # 接受1024的数据
            print('11')
            messageBytes = self.socket.recv(1024)
            message = str(messageBytes, encoding = 'utf-8')
            print(message)


if __name__ == '__main__':
    # cilentName = input('请输入昵称：')
    # 在主函数中输入名字，初始化的时候直接使用
    cilentName = 'lilian'
    cilent = cilentChat(cilentName)
    cilent.sendName()
    print('请注意消息发送格式为[<name>]:<message>!!!')
    try:
        send = Thread(target = cilent.sendMessage)
        recv = Thread(target = cilent.recvMessage)
        send.start()
        recv.start()
    except Exception as e:
        logging.exception(e)




























