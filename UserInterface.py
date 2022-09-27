from main import config, config_file
import blocker
import blockerwebsite
import blockerapplication
import localserver
import time
import sys
import os
import pystray
import PIL.Image
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QStackedWidget, QTableWidgetItem, QFileDialog, QTimeEdit, \
    QGroupBox, QFormLayout, QSizePolicy, QStyle, QMainWindow
from PyQt5.QtCore import QThread, QTime, pyqtSignal, Qt


class Worker1(QThread):
    def run(self):
        blocker.start_block()

class Worker2(QThread):
    def run(self):
        localserver.start()

class Worker3(QThread):
    lockSig = pyqtSignal()
    unlockSig = pyqtSignal()
    def run(self):
        while True:
            if blocker.should_block():
                if os.system(f'tasklist | find "Taskmgr.exe"') == 0 and blocker.should_blockTaskManager():  os.system(f"taskkill /im taskmgr.exe /f")
                time.sleep(2)
                if blocker.should_lockscheduledblock():
                    self.lockSig.emit()
            else:
                self.unlockSig.emit()
                time.sleep(5)



class alertPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/alertPopup.ui", self)
        self.setMinimumSize(400,300)
        self.btn_alert.accepted.connect(self.alert_accept)
        self.btn_alert.rejected.connect(self.alert_rejected)


    def alert_accept(self):
        self.close()
        try:
            start_program()
        except:
            pass

    def alert_rejected(self):
        self.close()



# Code below adapted from stack overflow @yurisnm
class TitleBar(QDialog):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        loadUi("ui/titlebar.ui", self)
        self.toolbtn_close.clicked.connect(self.btn_close)
        self.toolbtn_minimize.clicked.connect(self.btn_minimize)
        self.toolbtn_maximize.clicked.connect(self.btn_maximize)
        self.max = False
        self.pressing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(event.globalPos() - self.clickPos)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None


    def HiddenAppClicked(self, icon, item):
        if str(item) == "Maximize":
            icon.stop()
            self.parent.show()
            self.show()
        elif str(item) == "Exit":
            icon.stop()
            self.parent.close()
            self.close()

    def btn_close(self):
        self.parent.hide()
        self.hide()
        image = PIL.Image.open("app_images/appicon.png")
        icon = pystray.Icon("appicon", image, menu=pystray.Menu(
            pystray.MenuItem("Maximize", self.HiddenAppClicked, default=True),
            pystray.MenuItem("Exit", self.HiddenAppClicked)
        ))
        icon.run()



    def btn_maximize(self):
        if self.max:
            self.max = False
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
            self.max = True


    def btn_minimize(self):
        self.parent.showMinimized()


# class adapted from Stack Overflow @musicamante
class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)
        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

        self.setStyleSheet("""
                background-color: transparent; 
        """)

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class MainWindow(QMainWindow):
    _gripSize = 1.5
    def __init__(self):
        super().__init__()
        self.worker1 = Worker1()
        self.worker1.start()

        self.worker2 = Worker2()
        self.worker2.start()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        loadUi("ui/mainwindow.ui", self)

        self.titleBar = TitleBar(self)
        self.scrollArea.setWidget(self.titleBar)

        self.setMinimumSize(1100, 920)

        # Resize sidegrips - class adapted from Stack Overflow @musicamante
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge),
        ]

        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]

        # setup pages
        self.homeWidget = HomeWidget()
        self.blockedSitesWidget = BlockedSitesWidget()
        self.blockedAppsWidget = BlockedAppsWidget()
        self.scheduleBlocksWidget = ScheduleBlocksWidget()

        self.stackedWidget.addWidget(self.homeWidget)
        self.stackedWidget.addWidget(self.blockedSitesWidget)
        self.stackedWidget.addWidget(self.blockedAppsWidget)
        self.stackedWidget.addWidget(self.scheduleBlocksWidget)

        # initalize centralized window button style
        self.btn_home.setStyleSheet(windowPushButtonStyle)
        self.current_button = "self.btn_home"

        # transition widget windows:
        self.btn_home.clicked.connect(lambda: self.transition_widget_win("self.btn_home"))
        self.btn_blockedWeb.clicked.connect(lambda: self.transition_widget_win("self.btn_blockedWeb"))
        self.btn_blockedApps.clicked.connect(lambda: self.transition_widget_win("self.btn_blockedApps"))
        self.btn_scheduleBlocks.clicked.connect(lambda: self.transition_widget_win("self.btn_scheduleBlocks"))


    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def transition_widget_win(self, button_name):
        exec(f"{self.current_button}.setStyleSheet(windowUnpushButtonStyle)")
        self.current_button = button_name
        exec(f"{self.current_button}.setStyleSheet(windowPushButtonStyle)")
        exec(f"self.stackedWidget.setCurrentIndex({button_index[button_name]})")





class HomeWidget(QWidget):
    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):
        loadUi("ui/home.ui", self)

        # signals to disable/enable checkboxes
        self.worker3 = Worker3()
        self.worker3.lockSig.connect(self.disable_schedule_buttons)
        self.worker3.unlockSig.connect(self.enable_schedule_buttons)
        self.worker3.start()

        # setting styles
        self.startBlockCheckBox.setStyleSheet(checkBoxStyle)
        self.startScheduledBlockCheckBox.setStyleSheet(checkBoxStyle)
        self.startLockScheduledBlock.setStyleSheet(checkBoxStyle)
        self.startBlockTaskManager.setStyleSheet(checkBoxStyle)

        # buttons
        self.startBlockCheckBox.stateChanged.connect(self.change_block)
        self.startScheduledBlockCheckBox.stateChanged.connect(self.change_scheduledblock)
        self.startLockScheduledBlock.stateChanged.connect(self.change_lockscheduledblock)
        self.startBlockTaskManager.stateChanged.connect(self.change_blocktaskmanager)




        # block button initalize
        initial_block = config['blocker']['block']
        initial_scheduledBlock = config['blocker']['scheduledblock']
        initial_lockScheduledBlock = config['blocker']['lockscheduledblock']
        initial_blockTaskManager = config['blocker']['blocktaskmanager']

        if initial_block == "on":
            self.startBlockCheckBox.setChecked(True)
        else:
            self.startBlockCheckBox.setChecked(False)

        if initial_scheduledBlock == "on":
            self.startScheduledBlockCheckBox.setChecked(True)
        else:
            self.startScheduledBlockCheckBox.setChecked(False)

        if initial_lockScheduledBlock == 'on':
            self.startLockScheduledBlock.setChecked(True)
        else:
            self.startLockScheduledBlock.setChecked(False)

        if initial_blockTaskManager == "on":
            self.startBlockTaskManager.setChecked(True)
        else:
            self.startBlockTaskManager.setChecked(False)



    def change_block(self):
        self.update_block_button()
        with open(config_file, 'w') as write_config:
            config.write(write_config)

    def change_scheduledblock(self):
        self.update_scheduledblock_button()
        with open(config_file, 'w') as write_config:
            config.write(write_config)

    def change_lockscheduledblock(self):
        self.update_lockscheduledblock_button()
        with open(config_file, 'w') as write_config:
            config.write(write_config)

    def change_blocktaskmanager(self):
        self.update_blocktaskmanager_button()
        with open(config_file, 'w') as write_config:
            config.write(write_config)


    def update_block_button(self):
        if self.startBlockCheckBox.isChecked():
            config['blocker']['block'] = 'on'
        else:
            config['blocker']['block'] = 'off'

    def update_scheduledblock_button(self):
        if self.startScheduledBlockCheckBox.isChecked():
            config['blocker']['scheduledblock'] = 'on'
        else:
            config['blocker']['scheduledblock'] = 'off'

    def update_lockscheduledblock_button(self):
        if self.startLockScheduledBlock.isChecked():
            config['blocker']['lockscheduledblock'] = 'on'
        else:
            config['blocker']['lockscheduledblock'] = 'off'

    def update_blocktaskmanager_button(self):
        if self.startBlockTaskManager.isChecked():
            config['blocker']['blocktaskmanager'] = 'on'
        else:
            config['blocker']['blocktaskmanager'] = 'off'

    def disable_schedule_buttons(self):
        self.startScheduledBlockCheckBox.setEnabled(False)
        self.startLockScheduledBlock.setEnabled(False)

    def enable_schedule_buttons(self):
        self.startScheduledBlockCheckBox.setEnabled(True)
        self.startLockScheduledBlock.setEnabled(True)



class BlockedSitesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/blockedweb.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)

        # load in existing table items
        self.load_items()

        # table buttons
        self.btn_add.clicked.connect(self.add_item)
        self.blockSiteTextBox.returnPressed.connect(self.add_item)
        self.btn_delete.clicked.connect(self.remove_item)

    def load_items(self):
        blocked_sites = blockerwebsite.blocked_WEB()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites)/2)

        for site in blocked_sites:
            if site[:4] != 'www.':
                item = QTableWidgetItem(site)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, 0, item)
                row += 1



    def add_item(self):
        value = self.blockSiteTextBox.text()
        if value:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, item)
            blockerwebsite.add_block(value)
        else:
            print("Enter non-empty address")

        self.blockSiteTextBox.clear()

    def remove_item(self):
        if self.tableWidget.currentRow() != -1 and self.tableWidget.rowCount() > 0:
            hostname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerwebsite.delete_block(hostname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())




class BlockedAppsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/blockedapps.ui", self)
        self.tableWidget.verticalHeader().setVisible(False)

        # load in existing table items
        self.load_items()

        # table buttons
        self.btn_addApp.clicked.connect(self.add_item)
        self.btn_deleteApp.clicked.connect(self.remove_item)

    def load_items(self):
        blocked_sites = blockerapplication.blocked_APPS()
        row=0
        self.tableWidget.setRowCount(len(blocked_sites))

        for site in blocked_sites:
            item = QTableWidgetItem(site)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(row, 0, item)
            row += 1

    def add_item(self):
        application_name = QFileDialog.getOpenFileName(self, "Open File", "C:/", "All Files (*)")
        appname = application_name[0].split("/")[-1]
        if len(appname) != 0:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            item = QTableWidgetItem(appname)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)
            blockerapplication.add_block(appname)

    def remove_item(self):
        if self.tableWidget.currentRow() != -1 and self.tableWidget.rowCount() > 0:
            appname = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            blockerapplication.delete_block(appname)
            self.tableWidget.removeRow(self.tableWidget.currentRow())




class ScheduleBlocksWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi("ui/scheduleblocks.ui", self)

        #schedule blocks windows
        self.btn_scheduleMonday.clicked.connect(lambda: self.schedule_block("Monday"))
        self.btn_scheduleTuesday.clicked.connect(lambda: self.schedule_block("Tuesday"))
        self.btn_scheduleWednesday.clicked.connect(lambda: self.schedule_block("Wednesday"))
        self.btn_scheduleThursday.clicked.connect(lambda: self.schedule_block("Thursday"))
        self.btn_scheduleFriday.clicked.connect(lambda: self.schedule_block("Friday"))
        self.btn_scheduleSaturday.clicked.connect(lambda: self.schedule_block("Saturday"))
        self.btn_scheduleSunday.clicked.connect(lambda: self.schedule_block("Sunday"))

        self.tableWidget.setColumnCount(7)
        self.tableWidget.resizeRowsToContents()
        self.create_time_tables()
        for row in range(144):
            self.tableWidget.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.horizontalHeader().setVisible(False)

        self.color_time_tables()



    def create_time_tables(self):
        for column in range(7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            for row in range(144):
                item = QTableWidgetItem()
                item.setBackground(QBrush(QColor(255, 255, 255)))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                exec(f"self.tableWidget.setItem({row}, {column}, item)")


    def reset_time_tables(self):
        for column in range(7):
            for row in range(144):
                exec(f"self.tableWidget.item({row}, {column}).setBackground(QBrush(QColor(255, 255, 255)))")

    def color_time_tables(self):
        data = blocker.read_blocks()
        for day in data:
            column = blocker.date_to_value[day]
            for block in data[day].values():
                hour_start = int(block[0][:2])
                hour_end = int(block[1][:2])

                min_start = int(block[0][3:4])
                min_end = int(block[1][3:4])
                print(block)
                if min_start > 0:
                    start_block = hour_start * 6 + min_start
                else:
                    start_block = hour_start * 6

                if min_end > 0:
                    end_block = hour_end * 6 + min_end
                else:
                    end_block = hour_end * 6

                print(start_block, end_block)

                for period in range(start_block, end_block):
                    exec(f"self.tableWidget.item({period}, {column}).setBackground(QBrush(QColor(135, 206, 235)))")



    def update_time_tables(self):
        self.reset_time_tables()
        self.color_time_tables()

    def schedule_block(self, day):
        self.schedule_block_popup = ScheduleBlocksPopupWindow(day)
        self.schedule_block_popup.sig.connect(self.update_time_tables)
        self.schedule_block_popup.show()





class ScheduleBlocksPopupWindow(QWidget):
    sig = pyqtSignal()

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


    def addTimeWidget(self):
        row = len(self.timeEdits) + 1
        time_editFrom = TimeEdit()
        time_editTo = TimeEdit()
        self.form_layout.addRow(time_editFrom, time_editTo)
        self.timeEdits[row] = [time_editFrom, time_editTo]

    def deleteTimeWidget(self):

        row = len(self.timeEdits)
        if row >= 1:
            self.form_layout.removeRow(row-1)
            del self.timeEdits[row]
            try:
                blocker.remove_block(row, self.day)
            except:
                pass

    def closeEvent(self, event):
        self.sig.emit()

    def apply(self):
        blocker.add_block(self.day, self.timeEdits.items())
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
    alertWin = alertPopup()
    alertWin.show()

    sys.exit(app.exec_())



def start_program():
    global Window
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())





app = QApplication(sys.argv)


# setting up global UI variables
button_index = {"self.btn_home": 0, "self.btn_blockedWeb": 1, "self.btn_blockedApps": 2, "self.btn_scheduleBlocks": 3}

windowUnpushButtonStyle = """
    QPushButton {
	color: white;
	font: 63 12pt "Cascadia Mono SemiBold";
	background-color: rgb(24,24,24);
	border: 0;
    }

    QPushButton::hover {
	    background-color: black;
    }
"""

windowPushButtonStyle = """
    QPushButton {
	    color: white;
	    font: 63 12pt "Cascadia Mono SemiBold";
	    background-color: black;
	    border: 0;
    }

"""

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