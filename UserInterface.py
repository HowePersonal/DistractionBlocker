import blocker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
import sys




class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Distraction Blocker")
        self.setGeometry(0, 0, 400, 400)
        self.initUI()

    def initUI(self):
        self.history_btn = QtWidgets.QPushButton(self)
        self.history_btn.setText("Blocked Websites")
        self.history_btn.clicked.connect(self.click_blocked)

    def click_blocked(self):
        self.update()

    def update(self):
        self.label.adjustSize()



def start():
    app = QApplication(sys.argv)
    UI = Window()
    UI.show()
    sys.exit(app.exec_())

start()


