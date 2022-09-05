from main import config, config_file
import blocker
import blockerwebsite
import blockerapplication
import localserver
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QStackedWidget, QTableWidgetItem, QFileDialog, QTimeEdit, QGroupBox, QFormLayout
from PyQt5.QtCore import QThread, QTime


class Worker1(QThread):
    def run(self):
        blocker.start_block()

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

        try:
            start_program()
        except:
            pass

    def alert_rejected(self):
        self.close()




class HomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/home.ui", self)

        # setting styles
        self.startBlockCheckBox.setStyleSheet(checkBoxStyle)

        # transition windows
        self.btn_blockedWeb.clicked.connect(self.go_web_win)
        self.btn_blockedApps.clicked.connect(self.go_app_win)
        self.btn_scheduleBlocks.clicked.connect(self.go_schedule_win)

        # buttons
        self.startBlockCheckBox.stateChanged.connect(self.start_block)

        # start button initalize
        self.update_start_button()

    def start_block(self):
        self.update_start_button()
        with open(config_file, 'w') as write_config:
            config.write(write_config)

    def update_start_button(self):
        if self.startBlockCheckBox.isChecked():
            config['blocker']['block'] = 'on'
        else:
            config['blocker']['block'] = 'off'


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
        self.tableWidget.setRowCount(len(blocked_sites)/2)

        for site in blocked_sites:
            if site[:4] != 'www.':
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

        #schedule blocks windows
        self.btn_scheduleMonday.clicked.connect(lambda: self.schedule_block("Monday"))
        self.btn_scheduleTuesday.clicked.connect(lambda: self.schedule_block("Tuesday"))
        self.btn_scheduleWednesday.clicked.connect(lambda: self.schedule_block("Wednesday"))
        self.btn_scheduleThursday.clicked.connect(lambda: self.schedule_block("Thursday"))
        self.btn_scheduleFriday.clicked.connect(lambda: self.schedule_block("Friday"))
        self.btn_scheduleSaturday.clicked.connect(lambda: self.schedule_block("Saturday"))
        self.btn_scheduleSunday.clicked.connect(lambda: self.schedule_block("Sunday"))

    def go_home_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)

    def go_web_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def go_app_win(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def schedule_block(self, day):
        self.schedule_block_popup = ScheduleBlocksPopupWindow(day)
        self.schedule_block_popup.show()



class ScheduleBlocksPopupWindow(QWidget):
    def __init__(self, day):
        super().__init__()
        self.day = day
        self.init_ui(day)


    def init_ui(self, day):
        loadUi("ui/scheduleblockspopup.ui", self)
        self.dayLabel.setText(day)
        self.form_layout = QFormLayout()
        self.group_box = QGroupBox("")
        self.group_box.setLayout(self.form_layout)
        self.scrollArea.setWidget(self.group_box)


        # buttons
        self.btn_apply.clicked.connect(self.apply)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_addTime.clicked.connect(self.addTimeWidget)
        self.btn_deleteTime.clicked.connect(self.deleteTimeWidget)

        self.timeEdits = {}
        self.loadTimeWidgets()

    def loadTimeWidgets(self):
        data = blocker.read_blocks()
        for i, blocks in data[self.day].items():
            timesFromSplit = blocks[0].split(":")
            timeFrom = QTime(int(timesFromSplit[0]), int(timesFromSplit[1]), int(timesFromSplit[2]))

            timesToSplit = blocks[1].split(":")
            timeTo = QTime(int(timesToSplit[0]), int(timesToSplit[1]), int(timesToSplit[2]))

            time_editFrom = TimeEdit(timeFrom)
            time_editTo = TimeEdit(timeTo)

            self.form_layout.addRow(time_editFrom, time_editTo)
            self.timeEdits[int(i)] = [time_editFrom, time_editTo]
        print(self.timeEdits)

    def addTimeWidget(self):
        row = len(self.timeEdits) + 1
        time_editFrom = TimeEdit()
        time_editTo = TimeEdit()
        self.form_layout.addRow(time_editFrom, time_editTo)
        self.timeEdits[row] = [time_editFrom, time_editTo]
        print(row)

    def deleteTimeWidget(self):

        row = len(self.timeEdits)


        if row >= 1:
            self.form_layout.removeRow(row-1)
            del self.timeEdits[row]
            try:
                blocker.remove_block(row, self.day)
            except:
                pass


    def apply(self):
        for row, time in self.timeEdits.items():
            blocker.add_block(row, self.day, time[0].time().toString(), time[1].time().toString())
        self.close()

    def cancel(self):
        self.close()

class TimeEdit(QTimeEdit):
    def __init__(self, time=None):
        if time == None:
            super().__init__()
        else:
            super().__init__(time)
        self.setFixedSize(125, 20)




def confirm_start():
    global widget
    widget = QStackedWidget()
    alertWin = alertPopup()
    alertWin.show()

    sys.exit(app.exec_())



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
    sys.exit(app.exec_())





app = QApplication(sys.argv)

checkBoxStyle = """
    QCheckBox::indicator {
	    width: 50px;
	    height: 50px;
    }

    QCheckBox::indicator::checked {
	    image: url("ui/iconUI/toggle-on-button.png");
    }

    QCheckBox::indicator::unchecked {
	    image: url("ui/iconUI/toggle-off-button.png");
    }
    """


