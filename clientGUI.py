# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientGUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.registerNmae = QtWidgets.QLabel(self.centralwidget)
        self.registerNmae.setGeometry(QtCore.QRect(150, 170, 67, 16))
        self.registerNmae.setObjectName("registerNmae")
        self.password = QtWidgets.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(150, 290, 67, 16))
        self.password.setObjectName("password")
        self.clientName = QtWidgets.QTextEdit(self.centralwidget)
        self.clientName.setGeometry(QtCore.QRect(323, 160, 291, 31))
        self.clientName.setObjectName("clientName")
        self.clientPassword = QtWidgets.QTextEdit(self.centralwidget)
        self.clientPassword.setGeometry(QtCore.QRect(323, 280, 291, 31))
        self.clientPassword.setObjectName("clientPassword")
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        self.menuRouzip = QtWidgets.QMenu(self.menubar)
        self.menuRouzip.setObjectName("menuRouzip")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menuRouzip.addSeparator()
        self.menuRouzip.addAction(self.action_3)
        self.menuRouzip.addAction(self.action_2)
        self.menubar.addAction(self.menuRouzip.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.registerNmae.setText(_translate("MainWindow", "用户名"))
        self.password.setText(_translate("MainWindow", "密码"))
        self.loginButton.setText(_translate("MainWindow", "登录"))
        self.registerButton.setText(_translate("MainWindow", "注册"))
        self.label.setText(_translate("MainWindow", "Rouzip的聊天室"))
        self.menuRouzip.setTitle(_translate("MainWindow", "Rouzip的聊天室"))
        self.action_2.setText(_translate("MainWindow", "关闭"))
        self.action_3.setText(_translate("MainWindow", "在线人员"))
