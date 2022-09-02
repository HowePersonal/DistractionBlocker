import blocker
import blockerwebsite
import blockerapplication
import localserver
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QThread


class Worker1(QThread):
    def run(self):
        blocker.start_appblock()

class Worker2(QThread):
    def run(self):
        localserver.start()




class alertPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/alertPopup.ui", self)
        self.btn_alert.accepted.connect(self.alert_accept)
        self.btn_alert.rejected.connect(self.alert_rejected)

    def alert_accept(self):
        self.close()
        self.worker1 = Worker1()
        self.worker1.start()

        self.worker2 = Worker2()
        self.worker2.start()

        start_program()

    def alert_rejected(self):
        self.close()




class HomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/home.ui", self)

        # transition windows
        self.btn_blockedWeb.clicked.connect(self.go_web_win)
        self.btn_blockedApps.clicked.connect(self.go_app_win)
        self.btn_scheduleBlocks.clicked.connect(self.go_schedule_win)

    def go_web_win(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_app_win(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def go_schedule_win(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)


class BlockedSitesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/blockedweb.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)
        self.load_items()

        self.btn_add.clicked.connect(self.add_item)
        self.blockSiteTextBox.returnPressed.connect(self.add_item)
        self.btn_delete.clicked.connect(self.remove_item)

        #transition windows
        self.btn_home.clicked.connect(self.go_home_win)
        self.btn_blockedApps.clicked.connect(self.go_app_win)
        self.btn_scheduleBlocks.clicked.connect(self.go_schedule_win)

    def load_items(self):
        blocked_sites = blockerwebsite.blocked_WEB()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site in blocked_sites:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            row += 1

    def add_item(self):
        value = self.blockSiteTextBox.text()
        if value:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(value))
            blockerwebsite.add_block(value)
        else:
            print("Enter non-empty address")

        self.blockSiteTextBox.clear()

    def remove_item(self):
        if self.tableWidget.rowCount() > 0:
            hostname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerwebsite.delete_block(hostname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def go_home_win(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def go_app_win(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_schedule_win(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)




class BlockedAppsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/blockedapps.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)

        self.load_items()

        self.btn_addApp.clicked.connect(self.add_item)
        self.btn_deleteApp.clicked.connect(self.remove_item)

        # transition windows
        self.btn_home.clicked.connect(self.go_home_win)
        self.btn_blockedWeb.clicked.connect(self.go_web_win)
        self.btn_scheduleBlocks.clicked.connect(self.go_schedule_win)

    def load_items(self):
        blocked_sites = blockerapplication.blocked_APPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site in blocked_sites:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(site))
            row += 1

    def add_item(self):
        application_name = QFileDialog.getOpenFileName(self, "Open File", "C:/", "All Files (*)")
        appname = application_name[0].split("/")[-1]

        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(appname))
        blockerapplication.add_block(appname)

    def remove_item(self):
        if self.tableWidget.rowCount() > 0:
            appname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerapplication.delete_block(appname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def go_home_win(self):
        widget.setCurrentIndex(widget.currentIndex()-2)

    def go_web_win(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def go_schedule_win(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)




class ScheduleBlocksWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/scheduleblocks.ui", self)

        #transition windows
        self.btn_home.clicked.connect(self.go_home_win)
        self.btn_blockedWeb.clicked.connect(self.go_web_win)
        self.btn_blockedApps.clicked.connect(self.go_app_win)

    def go_home_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)

    def go_web_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def go_app_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)




def confirm_start():
    global widget
    widget = QStackedWidget()
    alertWin = alertPopup()
    alertWin.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")



def create_windows():
    home_win = HomeWindow()
    widget.addWidget(home_win)

    blocked_sites_win = BlockedSitesWindow()
    widget.addWidget(blocked_sites_win)

    blocked_apps_win = BlockedAppsWindow()
    widget.addWidget(blocked_apps_win)

    schedule_blocks_win = ScheduleBlocksWindow()
    widget.addWidget(schedule_blocks_win)


def start_program():
    create_windows()

    widget.resize(800, 500)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")


app = QApplication(sys.argv)

