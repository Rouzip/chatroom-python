# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatNew.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import datetime
import random
import requests
import hashlib
from bs4 import BeautifulSoup
from collections import deque
import logging
import os
from threading import Thread, Lock

from clientFunc import clientChat

# 存放访问的设定
# head 和　超时时间
head = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
Timeout = 1


# 存储地址　初始URL
url = "http://www.meizitu.com/"
path = '/home/rouzip/chatroom-python/picture/'


nameSet = set()
visited = set()


class chatWindow(object):

    def __init__(self, clientChat):
        def pictureSpider(url, visited, nameSet):
            # 存放要遍历的网站
            stack = deque()
            stack.append(url)
            while stack:
                try:
                    picUrl = stack.popleft()
                    visited.add(picUrl)
                    response = requests.session().get(
                        picUrl, headers=head, timeout=Timeout)
                    bsp = BeautifulSoup(response.content, 'lxml')
                    webList = bsp.find_all('a')
                    for webText in webList:
                        webUrl = webText.get('href')
                        # BFS 遍历，将本页链接全部加入到已浏览
                        if webUrl and webUrl not in visited:
                            stack.append(webUrl)

                    photoList = bsp.find_all('img')
                    for photoText in photoList:
                        photoUrl = photoText.get('src')
                        if 'erweima' in photoUrl:
                            continue  # 不要二维码的图片
                        if 'limg' in photoUrl:
                            continue  # 不要小图
                        if 'templets' in photoUrl:
                            continue  # 不要模板图
                        try:
                            # 使用md5函数对名字进行缩略
                            temp = hashlib.md5()
                            temp.update(bytes(photoUrl, encoding='utf-8'))
                            photoName = temp.hexdigest()
                            if photoUrl and photoName not in nameSet:
                                photo = requests.session().get(
                                    photoUrl, headers=head, timeout=Timeout)
                                with open(path+photoName+'.jpg', 'wb') as fp:
                                    fp.write(photo.content)
                                nameSet.add(photoName)
                            pictureNum = os.listdir(
                                '/home/rouzip/chatroom-python/picture')
                            if len(pictureNum) >= 10:
                                return
                        except Exception as g:
                            logging.exception(g)
                except Exception:
                    pass
        self.client = clientChat
        pictureSpider(url, visited, nameSet)
        # 消息暂存变量
        self.message = []
        # 锁变量
        self.q = Lock()
        self.time = QTimer()
        try:
            Thread(target=self.receive).start()
        except Exception as e:
            logging.exception(e)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(866, 749)
        self.chatmsg_textEdit = QtWidgets.QTextEdit(Dialog)
        self.chatmsg_textEdit.setGeometry(QtCore.QRect(50, 30, 471, 471))
        self.chatmsg_textEdit.setObjectName("chatmsg_textEdit")
        self.sendmsg_textEdit = QtWidgets.QTextEdit(Dialog)
        self.sendmsg_textEdit.setGeometry(QtCore.QRect(50, 520, 471, 201))
        self.sendmsg_textEdit.setObjectName("sendmsg_textEdit")
        self.send_btn = QtWidgets.QPushButton(Dialog)
        self.send_btn.setGeometry(QtCore.QRect(640, 570, 99, 27))
        self.send_btn.setObjectName("send_btn")
        self.clear_btn = QtWidgets.QPushButton(Dialog)
        self.clear_btn.setGeometry(QtCore.QRect(640, 650, 99, 27))
        self.clear_btn.setObjectName("clear_btn")
        self.image_label = QtWidgets.QLabel(Dialog)
        self.image_label.setGeometry(QtCore.QRect(570, 80, 231, 291))
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        pixmap = self.randomPic()

        self.image_label.setPixmap(pixmap.scaled(200, 300, 0))
        ################事件处理函数###################
        self.clear_btn.clicked.connect(self.clean)
        self.send_btn.clicked.connect(self.send)
        self.time.timeout.connect(self.receiveMsg)
        self.time.start(10)

    def receiveMsg(self):
        #################消息显示#########################
        if not len(self.message):
            pass
        else:
            for pos, msg in enumerate(self.message):
                self.q.acquire()
                self.chatmsg_textEdit.append(msg)
                self.message.pop(pos-1)
                self.q.release()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.send_btn.setText(_translate("Dialog", "发送"))
        self.clear_btn.setText(_translate("Dialog", "清除"))

    #　随机函数挑选出 放在label中的图片
    def randomPic(self):
        random.seed(datetime.datetime.now())
        pictureNameList = os.listdir('/home/rouzip/chatroom-python/picture')
        pictureName = pictureNameList[
            random.randint(0, len(pictureNameList) - 1)]
        pixmap = QPixmap('/home/rouzip/chatroom-python/picture/' + pictureName)
        return pixmap

    # 发送自己的消息，并将消息清除
    def send(self):
        try:
            message = self.sendmsg_textEdit.toPlainText()
            self.client.sendMessage(message)
            self.clean()
        except Exception as e:
            logging.exception(e)

    # 清除聊天窗口中自己发送的消息
    def clean(self):
        self.sendmsg_textEdit.clear()

    # 接受到socket的信息，然后拼接到chatmsg_textEdit之上。
    def receive(self):
        try:
            while True:
                messageByte = self.client.recvMsg()
                message = str(messageByte, encoding='utf-8')
                self.message.append(message)
        except Exception as e:
            logging.exception(e)

    # 退出的时候向服务器发送退出信息
    def closeEvent(self, event):
        self.client.sendMessage(bytes('quit', encoding='utf-8'))
        event.accept()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    client = clientChat()
    client.initName('a')
    ui = chatWindow(client)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
