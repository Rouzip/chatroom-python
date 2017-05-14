# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_chating(object):
    def setupUi(self, chating):
        chating.setObjectName("chating")
        chating.resize(967, 664)
        self.sendmsg_textEdit = QtWidgets.QTextEdit(chating)
        self.sendmsg_textEdit.setGeometry(QtCore.QRect(30, 480, 611, 151))
        self.sendmsg_textEdit.setObjectName("sendmsg_textEdit")
        self.chatmsg_textEditl = QtWidgets.QTextEdit(chating)
        self.chatmsg_textEditl.setGeometry(QtCore.QRect(30, 30, 611, 411))
        self.chatmsg_textEditl.setObjectName("chatmsg_textEditl")
        self.image = QtWidgets.QTextEdit(chating)
        self.image.setGeometry(QtCore.QRect(670, 30, 271, 451))
        self.image.setObjectName("image")
        self.send_btn = QtWidgets.QPushButton(chating)
        self.send_btn.setGeometry(QtCore.QRect(720, 520, 99, 27))
        self.send_btn.setObjectName("send_btn")
        self.clear_btn = QtWidgets.QPushButton(chating)
        self.clear_btn.setGeometry(QtCore.QRect(720, 580, 99, 27))
        self.clear_btn.setObjectName("clear_btn")

        self.retranslateUi(chating)
        QtCore.QMetaObject.connectSlotsByName(chating)

    def retranslateUi(self, chating):
        _translate = QtCore.QCoreApplication.translate
        chating.setWindowTitle(_translate("chating", "Form"))
        self.send_btn.setText(_translate("chating", "发送"))
        self.clear_btn.setText(_translate("chating", "清除"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chating = QtWidgets.QWidget()
    ui = Ui_chating()
    ui.setupUi(chating)
    chating.show()
    sys.exit(app.exec_())

