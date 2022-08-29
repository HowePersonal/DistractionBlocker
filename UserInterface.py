import blockerwebsite
import blockerapplication
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTableWidgetItem, QFileDialog




class alertPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/alertPopup.ui", self)
        self.btn_alert.accepted.connect(self.alertAccept)
        self.btn_alert.rejected.connect(self.alertRejected)

    def alertAccept(self):
        self.close()
        start()

    def alertRejected(self):
        self.close()




class HomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/home.ui", self)

        # transition windows
        self.btn_blockedHistory.clicked.connect(self.goBlockedWebWindow)
        self.btn_blockedApps.clicked.connect(self.goBlockedAppWindow)

    def goBlockedWebWindow(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def goBlockedAppWindow(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)


class BlockedSitesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/blockedhistory.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0, 638)
        self.loaditems()

        #transition windows
        self.btn_home.clicked.connect(self.goHomeWindow)
        self.btn_blockedApps.clicked.connect(self.goBlockedAppWindow)

        self.btn_add.clicked.connect(self.addItem)
        self.blockSiteTextBox.returnPressed.connect(self.addItem)
        self.btn_delete.clicked.connect(self.removeItem)

    def loaditems(self):
        blocked_sites = blockerwebsite.blocked_IPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site in blocked_sites.keys():
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            row += 1

    def addItem(self):
        value = self.blockSiteTextBox.text()
        if value:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(value))
            blockerwebsite.add_block(value)
        else:
            print("Enter non-empty address")

        self.blockSiteTextBox.clear()

    def removeItem(self):
        if self.tableWidget.rowCount() > 0:
            hostname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerwebsite.delete_block(hostname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def goHomeWindow(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def goBlockedAppWindow(self):
        widget.setCurrentIndex(widget.currentIndex()+1)


class BlockedAppsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("ui/blockedapps.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0, 638)

        self.loaditems()

        self.btn_addApp.clicked.connect(self.addItem)
        self.btn_deleteApp.clicked.connect(self.removeItem)

        # transition windows
        self.btn_home.clicked.connect(self.goHomeWindow)
        self.btn_blockedHistory.clicked.connect(self.goBlockedWebWindow)



    def loaditems(self):
        blocked_sites = blockerapplication.blocked_APPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site in blocked_sites:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            row += 1


    def addItem(self):
        application_name = QFileDialog.getOpenFileName(self, "Open File", "C:/", "All Files (*)")
        appname = application_name[0].split("/")[-1]

        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(appname))
        blockerapplication.add_block(appname)

    def removeItem(self):
        if self.tableWidget.rowCount() > 0:
            appname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerwebsite.delete_block(appname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())


    def goBlockedWebWindow(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def goHomeWindow(self):
        widget.setCurrentIndex(widget.currentIndex()-2)





def confirm_start():
    global widget
    widget = QStackedWidget()
    alertWin = alertPopup()
    alertWin.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")



def createWindows():
    homeWin = HomeWindow()
    widget.addWidget(homeWin)

    blockedSitesWin = BlockedSitesWindow()
    widget.addWidget(blockedSitesWin)

    blockedAppsWin = BlockedAppsWindow()
    widget.addWidget(blockedAppsWin)


def start():
    blockerwebsite.close_browsers()
    createWindows()

    widget.resize(800, 500)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")

app = QApplication(sys.argv)
