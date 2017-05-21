# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientGUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
import logging
import os

from clientFunc import clientChat
from clientSignup import Ui_Dialog
from chatNew import chatWindow


class Ui_mainWindow(object):

    def __init__(self, clientChat):
        self.client = clientChat

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "../下载/chat_128px_1201543_easyicon.net.ico"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.registerNmae = QtWidgets.QLabel(self.centralwidget)
        self.registerNmae.setGeometry(QtCore.QRect(150, 170, 67, 16))
        self.registerNmae.setObjectName("registerNmae")
        self.password = QtWidgets.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(150, 290, 67, 17))
        self.password.setObjectName("password")
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(240, 430, 99, 27))
        self.loginButton.setObjectName("loginButton")
        self.registerButton = QtWidgets.QPushButton(self.centralwidget)
        self.registerButton.setGeometry(QtCore.QRect(500, 430, 99, 27))
        self.registerButton.setObjectName("registerButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 60, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Tlwg Mono")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.userName = QtWidgets.QLineEdit(self.centralwidget)
        self.userName.setGeometry(QtCore.QRect(310, 170, 191, 27))
        self.userName.setAcceptDrops(True)
        self.userName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userName.setObjectName("userName")
        self.userPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.userPassword.setGeometry(QtCore.QRect(310, 290, 191, 27))
        self.userPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userPassword.setObjectName("userPassword")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action_close = QtWidgets.QAction(mainWindow)
        self.action_close.setObjectName("action_close")
        self.action_personalive = QtWidgets.QAction(mainWindow)
        self.action_personalive.setObjectName("action_personalive")
        self.action_login = QtWidgets.QAction(mainWindow)
        self.action_login.setObjectName("action_login")
        self.registerNmae.setBuddy(self.userName)
        self.password.setBuddy(self.userPassword)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        mainWindow.setTabOrder(self.userName, self.userPassword)
        mainWindow.setTabOrder(self.userPassword, self.loginButton)
        mainWindow.setTabOrder(self.loginButton, self.registerButton)

        self.center()

    def center(self):  # 主窗口居中显示函数

        screen = QDesktopWidget().screenGeometry()
        size = mainWindow.geometry()
        mainWindow.move((screen.width()-size.width())/2,
                        (screen.height()-size.height())/2)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "聊天室"))
        self.registerNmae.setText(_translate("mainWindow", "用户名"))
        self.password.setText(_translate("mainWindow", "密码"))
        self.loginButton.setText(_translate("mainWindow", "登录"))
        self.registerButton.setText(_translate("mainWindow", "注册"))
        self.label.setText(_translate("mainWindow", "Rouzip的聊天室"))
        self.action_close.setText(_translate("mainWindow", "关闭"))
        self.action_close.setShortcut(_translate("mainWindow", "Ctrl+W"))
        self.action_personalive.setText(_translate("mainWindow", "在线人员"))
        self.action_personalive.setShortcut(_translate("mainWindow", "Ctrl+S"))
        self.action_login.setText(_translate("mainWindow", "登录"))

        ###############事件处理函数#####################
        self.loginButton.clicked.connect(self.chat)
        self.registerButton.clicked.connect(self.signUp)

    def signUp(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog(self.client)
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
        return

    '''
    需要改进，按钮无法响应函数，需要进行debug
    验证放在这里，然后chat负责接受名字，逻辑更清楚一些
    '''

    def chat(self):
        try:
            name = self.userName.text()
            password = self.userPassword.text()
            for word in password:
                if word == ' ':
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Warning)
                    error.setWindowTitle('错误！')
                    error.setText('密码中不该包含空格')
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()
                    return
            if not name or not password:
                error = QMessageBox()
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle('错误！')
                error.setText('请填写登录信息')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
            passwordList = []
            '''
            从hash链中倒置使用，发送密码
            '''
            try:
                with open(os.getcwd()+'/'+name+'.txt', 'r') as fp:
                    passwordLoc = fp.readline().strip()

                    if password != passwordLoc:
                        # 检测是否输入正确的密码
                        '''
                        我的构想本程序只是用于加密信道的传输，密码只是为了不是误操作
                        和不是别人登录自己的账号，以后skey协议应该还可以改进

                        '''
                        error = QMessageBox()
                        error.setIcon(QMessageBox.Warning)
                        error.setWindowTitle('错误！')
                        error.setText('密码错误！')
                        error.setStandardButtons(QMessageBox.Ok)
                        error.exec_()
                        return
                    passwordList.append(passwordLoc)
                    passwordList += fp.read().split('\n')
                    for pos, line in enumerate(passwordList):
                        if line.find('usethis') != -1:
                            password = line.strip()
                            if pos - 1 == 0:
                                error = QMessageBox()
                                error.setIcon(QMessageBox.Warning)
                                error.setWindowTitle('错误！')
                                error.setText('hash链已使用完！')
                                error.setStandardButtons(QMessageBox.Ok)
                                error.exec_()
                                return
                            password = passwordList.pop(pos)[:32]
                            passwordList[pos - 1] += (' usethis')

            except Exception as e:
                logging.exception(e)

            self.client.sendMessage(name + ' ' + password)
            responseByte = self.client.recvMsg()
            if responseByte == b'\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x91':
                error = QMessageBox()
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle('错误！')
                error.setText('无此用户！')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
            if responseByte == b'\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x92':
                # 检测是否被人重放攻击
                error = QMessageBox()
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle('错误！')
                error.setText('密码错误！')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
            elif responseByte == b'\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x93':
                error = QMessageBox()
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle('错误！')
                error.setText('此用户已经在线！')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
            self.client.initName(name)
            try:
                with open(os.getcwd()+'/'+name+'.txt', 'w') as fp:
                    for line in filter(lambda w: w != passwordList[-1],
                                       passwordList):
                        fp.write(line+'\n')
                    else:
                        fp.write(passwordList[-1])
            except Exception as e:
                logging.exception(e)

            Dialog = QtWidgets.QDialog()
            ui = chatWindow(self.client)
            ui.setupUi(Dialog)
            Dialog.show()
            mainWindow.hide()
            Dialog.exec_()

        except Exception as e:
            logging.exception(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.sendMessage(bytes('quit', encoding='utf-8'))


if __name__ == "__main__":
    import sys
    client = clientChat()
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow(client)
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
