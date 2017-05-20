# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatNew.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

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

        self.send_btn.clicked.connect(self.pr)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.send_btn.setText(_translate("Dialog", "发送"))
        self.clear_btn.setText(_translate("Dialog", "清除"))

    def pr(self):
        message = self.sendmsg_textEdit.toPlainText()
        print(message)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
