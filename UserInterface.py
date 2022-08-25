import blocker
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget


class HomeWindow(QDialog):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        loadUi("ui/home.ui", self)
        self.btn_blockedHistory.clicked.connect(self.goBlockedWindow)

    def goBlockedWindow(self):
        blocked_sites_win = BlockedSitesWindow(self.widget)
        self.widget.addWidget(blocked_sites_win)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)


class BlockedSitesWindow(QDialog):
    def __init__(self, widget):
        self.widget = widget
        super().__init__()
        loadUi("ui/blockedhistory.ui", self)
        self.tableWidget.setColumnWidth(0, 319)
        self.tableWidget.setColumnWidth(1, 319)
        self.loaditems()
    def loaditems(self):
        blocked_sites = blocker.blocked_IPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site, ip in blocked_sites.items():
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(ip))
            row += 1



def start():
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    win = HomeWindow(widget)
    widget.addWidget(win)
    widget.setFixedHeight(500)
    widget.setFixedWidth(800)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")


