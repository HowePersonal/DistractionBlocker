import blocker
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget




class BlockedSitesWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("blockedhistory.ui", self)
        self.tableWidget.setColumnWidth(0, 385)
        self.tableWidget.setColumnWidth(1, 385)
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
    win = BlockedSitesWindow()
    widget = QStackedWidget()
    widget.addWidget(win)
    widget.setFixedHeight(500)
    widget.setFixedWidth(800)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")


