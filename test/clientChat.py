# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import datetime
import random
import requests
import hashlib
from bs4 import BeautifulSoup
from collections import deque
import logging
import os
import time

from clientFunc import clientChat

# 存放访问的设定
# head 和　超时时间
head = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
Timeout = 5


# 存储地址　初始URL
url = "http://www.meizitu.com/"
path = '/home/rouzip/chatroom-python/picture/'


nameSet = set()
visited = set()


class Ui_chating(object):
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
                                with open(path + photoName + '.jpg', 'wb') as fp:
                                    fp.write(photo.content)
                                nameSet.add(photoName)
                            pictureNum = os.listdir(
                                '/home/rouzip/chatroom-python/picture')
                            if len(pictureNum) >= 30:
                                return
                        except Exception as g:
                            logging.exception(g)
                except Exception as e:
                    logging.exception(e)
        self.client = clientChat
        pictureSpider(url, visited, nameSet)
        # time.sleep(3)

    def setupUi(self, chating):
        chating.setObjectName("chating")
        chating.resize(967, 664)
        self.sendmsg_textEdit = QtWidgets.QTextEdit(chating)
        self.sendmsg_textEdit.setGeometry(QtCore.QRect(30, 480, 611, 151))
        self.sendmsg_textEdit.setObjectName("sendmsg_textEdit")
        self.chatmsg_textEdit = QtWidgets.QTextEdit(chating)
        self.chatmsg_textEdit.setGeometry(QtCore.QRect(30, 30, 611, 411))
        self.chatmsg_textEdit.setObjectName("chatmsg_textEditl")
        self.send_btn = QtWidgets.QPushButton(chating)
        self.send_btn.setGeometry(QtCore.QRect(720, 520, 99, 27))
        self.send_btn.setObjectName("send_btn")
        self.clear_btn = QtWidgets.QPushButton(chating)
        self.clear_btn.setGeometry(QtCore.QRect(720, 580, 99, 27))
        self.clear_btn.setObjectName("clear_btn")
        self.label = QtWidgets.QLabel(chating)
        self.label.setGeometry(QtCore.QRect(670, 40, 251, 421))
        self.label.setObjectName("label")
        pixmap = self.randomPic()

        self.label.setPixmap(pixmap.scaled(200, 300, 0))

        self.retranslateUi(chating)
        QtCore.QMetaObject.connectSlotsByName(chating)

        ################事件处理函数###################
        self.clear_btn.clicked.connect(self.clean)


    def send(self):
        message = self.chatmsg_textEdit.toPlainText()
        print(message)
        self.client.send(message)
        self.clean()


    # 清除聊天窗口中自己发送的消息
    def clean(self):
        self.sendmsg_textEdit.clear()

    # 接受到socket的信息，然后拼接到chatmsg_textEdit之上。
    def receive(self):
        pass


    def retranslateUi(self, chating):
        _translate = QtCore.QCoreApplication.translate
        chating.setWindowTitle(_translate("chating", "Form"))
        self.send_btn.setText(_translate("chating", "发送"))
        self.clear_btn.setText(_translate("chating", "清除"))

    #　随机函数挑选出 放在label中的图片
    def randomPic(self):
        random.seed(datetime.datetime.now())
        pictureNameList = os.listdir('/home/rouzip/chatroom-python/picture')
        pictureName = pictureNameList[
            random.randint(0, len(pictureNameList) - 1)]
        pixmap = QPixmap('/home/rouzip/chatroom-python/picture/' + pictureName)
        return pixmap



    # 退出的时候向服务器发送退出信息
    def closeEvent(self, event):
        self.client.send(bytes('quit', encoding='utf-8'))
        event.accept()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chating = QtWidgets.QWidget()
    client = clientChat()
    ui = Ui_chating(client)
    ui.setupUi(chating)
    chating.show()
    sys.exit(app.exec_())
