from cilentFunc import *
from clientGUI import *
import sys
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow


class clientApplication(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(clientApplication, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = clientApplication()
    client.show()
    sys.exit(app.exec_())
