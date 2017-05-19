# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientGUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../下载/chat_128px_1201543_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

