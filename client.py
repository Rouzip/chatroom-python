from cilentFunc import *
from clientGUI import *
import sys
from PyQt5.Qt import QApplication


class clientApplication(Ui_MainWindow):

    def __init__(self):
        super(Ui_MainWindow).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = clientApplication()
    client.show()
    sys.exit(app.exec_())
