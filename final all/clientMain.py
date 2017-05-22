from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from PyQt5.QtWidgets import QWidget
import logging
import os

from clientFunc import clientChat
from clientSignup import Ui_Dialog
from clientChat import chatWindow


class clientMain(QtWidgets.QWidget):

    def __init__(self, clientChat):
        super(clientMain, self).__init__()
        self.client = clientChat

        self.setObjectName("mainWindow")
        self.resize(799, 599)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "../../下载/chat_128px_1201543_easyicon.net.ico"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(290, 80, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Tlwg Mono")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.password = QtWidgets.QLabel(self)
        self.password.setGeometry(QtCore.QRect(200, 340, 67, 17))
        self.password.setObjectName("password")
        self.registerNmae = QtWidgets.QLabel(self)
        self.registerNmae.setGeometry(QtCore.QRect(200, 210, 67, 16))
        self.registerNmae.setObjectName("registerNmae")
        self.registerButton = QtWidgets.QPushButton(self)
        self.registerButton.setGeometry(QtCore.QRect(460, 470, 99, 27))
        self.registerButton.setObjectName("registerButton")
        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setGeometry(QtCore.QRect(230, 470, 99, 27))
        self.loginButton.setObjectName("loginButton")
        self.userPassword = QtWidgets.QLineEdit(self)
        self.userPassword.setGeometry(QtCore.QRect(410, 340, 191, 27))
        self.userPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userPassword.setObjectName("userPassword")
        self.userName = QtWidgets.QLineEdit(self)
        self.userName.setGeometry(QtCore.QRect(410, 210, 191, 27))
        self.userName.setAcceptDrops(True)
        self.userName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userName.setObjectName("userName")
        self.password.setBuddy(self.userPassword)
        self.registerNmae.setBuddy(self.userName)

        self.retranslateUi()
        # QtCore.QMetaObject.connectSlotsByName(self)

        self.center()

    # 主窗口居中显示函数
    def center(self):

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
                  (screen.height()-size.height())/2)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "Rouzip的聊天室"))
        self.label.setText(_translate("mainWindow", "Rouzip的聊天室"))
        self.password.setText(_translate("mainWindow", "密码"))
        self.registerNmae.setText(_translate("mainWindow", "用户名"))
        self.registerButton.setText(_translate("mainWindow", "注册"))
        self.loginButton.setText(_translate("mainWindow", "登录"))

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

            chatroom = chatWindow(self.client, self)
            chatroom.show()
            self.hide()
            chatroom.exec_()

        except Exception as e:
            logging.exception(e)

    def closeEvent(self, event):
        print('关闭啦')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    client = clientChat()
    msgBox = clientMain(clientChat=client)
    msgBox.show()
    sys.exit(app.exec_())
