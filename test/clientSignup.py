# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signup.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import time

from clientFunc import clientChat


class Ui_Dialog(object):

    def __init__(self, clientChat):
        self.client = clientChat

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(752, 554)
        Dialog.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "../下载/Register_key_128px_510498_easyicon.net.ico"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(140, 120, 471, 291))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.userName_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.userName_lineEdit.setObjectName("userName_lineEdit")
        self.gridLayout.addWidget(self.userName_lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.email_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.gridLayout.addWidget(self.email_lineEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.password_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.gridLayout.addWidget(self.password_lineEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.password2_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.password2_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2_lineEdit.setObjectName("password2_lineEdit")
        self.gridLayout.addWidget(self.password2_lineEdit, 3, 1, 1, 1)
        self.signup_btn = QtWidgets.QPushButton(self.widget)
        self.signup_btn.setObjectName("signup_btn")
        self.gridLayout.addWidget(self.signup_btn, 4, 1, 1, 1)
        self.label.setBuddy(self.userName_lineEdit)
        self.label_2.setBuddy(self.email_lineEdit)
        self.label_3.setBuddy(self.password_lineEdit)
        self.label_4.setBuddy(self.password2_lineEdit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.userName_lineEdit, self.email_lineEdit)
        Dialog.setTabOrder(self.email_lineEdit, self.password_lineEdit)
        Dialog.setTabOrder(self.password_lineEdit, self.password2_lineEdit)
        Dialog.setTabOrder(self.password2_lineEdit, self.signup_btn)

        #######################事件处理函数###########
        self.signup_btn.clicked.connect(self.signUp)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "注册"))
        self.label.setText(_translate("Dialog", "用户名"))
        self.label_2.setText(_translate("Dialog", "注册邮箱"))
        self.label_3.setText(_translate("Dialog", "密码"))
        self.label_4.setText(_translate("Dialog", "确认密码"))
        self.signup_btn.setText(_translate("Dialog", "注册"))

    def signUp(self):
        name = self.userName_lineEdit.text()
        email = self.email_lineEdit.text()
        password1 = self.password_lineEdit.text()
        password2 = self.password2_lineEdit.text()
        for word in password1:
            if word == ' ':
                error = QMessageBox()
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle('错误！')
                error.setText('密码中不该包含空格')
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
        if not name:
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setWindowTitle('错误！')
            error.setText('请输入名字')
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
            return
        if not email:
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setWindowTitle('错误！')
            error.setText('请输入email')
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
            return
        if not password1:
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setWindowTitle('错误！')
            error.setText('请输入密码')
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
            return
        if not password1 == password2:
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setWindowTitle('错误！')
            error.setText('两次密码不同！')
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
            return
        self.client.sendMessage('注册')
        time.sleep(1)
        self.client.sendMessage(name + ' ' + email + ' ' + password1)
        ########就是接受不到数据########
        print('发送成功')
        responseByte = self.client.recvMsg()
        response = str(responseByte, encoding='utf-8')
        print('接受成功')
        if response == '失败':
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setWindowTitle('错误！')
            error.setText('用户名已使用，注册失败')
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
            return
        success = QMessageBox()
        success.setIcon(QMessageBox.Information)
        success.setWindowTitle('成功！')
        success.setText('恭喜注册成功！')
        success.setStandardButtons(QMessageBox.Ok)
        success.exec_()
        '''
        这里需要添加skey的接受
        '''
        return



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    test = clientChat()
    ui = Ui_Dialog(test)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
