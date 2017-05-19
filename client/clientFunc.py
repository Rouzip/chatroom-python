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

    def __init__(self, name):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(HOST)
        self.name = name

    # 向服务器发送自己的名字
    def sendName(self):
        self.socket.send(bytes(self.name, encoding='utf-8'))
        time.sleep(1)

    # 向服务器发送消息
    def sendMessage(self):
        while True:
            '''
            改为在gui端输入
            '''
            message = input('<<')
            '''
            改为在gui输出
            '''
            messageBytes = bytes(message, encoding='utf-8')
            self.socket.send(messageBytes)
            time.sleep(1)

    # 接受服务器发送的消息
    def recvMessage(self):
        while True:
            # 接受1024的数据
            messageBytes = self.socket.recv(1024)
            message = str(messageBytes, encoding='utf-8')
            '''
            改为在gui输出
            '''
            print(message)


if __name__ == '__main__':
    clientName = input('请输入昵称：')
    while not clientName:
        print('请重新输入昵称')
        clientName = input('请输入昵称：')
    # 在主函数中输入名字，初始化的时候直接使用
    client = clientChat(clientName)
    client.sendName()
    print('请注意消息发送格式为[<name>]:<message>!!!')
    # 两个线程分别管理输入与输出
    try:
        send = Thread(target=client.sendMessage)
        recv = Thread(target=client.recvMessage)
        send.start()
        recv.start()
    except Exception as e:
        logging.exception(e)
