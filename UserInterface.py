import blocker
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget


class HomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/home.ui", self)
        self.btn_blockedHistory.clicked.connect(self.goBlockedWindow)



    def goBlockedWindow(self):
        win = BlockedSitesWindow()
        widget.addWidget(win)
        widget.setCurrentIndex(widget.currentIndex()+1)




class BlockedSitesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/blockedhistory.ui", self)
        self.tableWidget.setColumnWidth(0, 319)
        self.tableWidget.setColumnWidth(1, 319)
        self.loaditems()
        self.btn_home.clicked.connect(self.goHomeWindow)

    def loaditems(self):
        blocked_sites = blocker.blocked_IPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site, ip in blocked_sites.items():
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(ip))
            row += 1

    def goHomeWindow(self):
        win = HomeWindow()
        widget.addWidget(win)
        widget.setCurrentIndex(widget.currentIndex()-1)







def start():
    app = QApplication(sys.argv)
    global widget
    widget = QStackedWidget()

    homeWin = HomeWindow()
    widget.addWidget(homeWin)

    widget.setFixedHeight(500)
    widget.setFixedWidth(800)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")


