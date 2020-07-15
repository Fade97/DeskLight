import serial
import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtCore import *
import com

buffer = []


class Updater(QThread):
    def run(self):
        com.send(buffer)


def clickable(widget):

    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        if event.button() == Qt.LeftButton:
                            self.obj = obj
                            self.clicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def rclickable(widget):

    class rFilter(QObject):

        rclicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.obj = obj
                        if event.button() == Qt.RightButton:
                            self.rclicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True

            return False

    filter = rFilter(widget)
    widget.installEventFilter(filter)
    return filter.rclicked


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.settings = QSettings("DeskLight")

        self.show()
        self.updater = Updater()
        self.updater.start()
        self.pbPickColor = self.findChild(QtWidgets.QPushButton, 'pbPickColor')
        self.pbRefresh = self.findChild(QtWidgets.QPushButton, 'pbRefresh')
        self.leColor = self.findChild(QtWidgets.QLineEdit, 'leColor')
        self.lColor = self.findChild(QtWidgets.QLabel, 'lColor')
        self.lColorSave = []
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave1'))
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave2'))
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave3'))
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave4'))
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave5'))
        self.lColorSave.append(self.findChild(QtWidgets.QLabel, 'lColorSave6'))

        self.mode = 1
        self.rbAnim_PerlinFade = self.findChild(
            QtWidgets.QRadioButton, 'rbAnim_PerlinFade')
        self.rbAnim_ArrowWaves = self.findChild(
            QtWidgets.QRadioButton, 'rbAnim_ArrowWaves')

        self.rbAnim_PerlinFade.toggled.connect(self.updateMode)
        self.rbAnim_ArrowWaves.toggled.connect(self.updateMode)

        self.updateMode()

        self.pbPickColor.clicked.connect(self.pickColor)
        self.pbRefresh.clicked.connect(self.refreshQue)

        for cSave in self.lColorSave:
            val = self.loadFromRegistry(cSave.objectName())
            if (isinstance(val, str)):
                cSave.setStyleSheet(
                    'background-color: ' + val)
            clickable(cSave).connect(self.loadColor)
            rclickable(cSave).connect(self.saveColor)

    def saveToRegistry(self, name, value):
        self.settings.setValue(name, value)

    def loadFromRegistry(self, name):
        return self.settings.value(name)

    def pickColor(self):
        self.color = QtWidgets.QColorDialog.getColor()
        if (self.color.isValid()):
            self.lColor.setStyleSheet(
                'background-color: ' + self.color.name(self.color.HexRgb))
            self.leColor.setText(self.color.name())
            print('<'+str(self.mode)+',' + str(self.color.red()) + ',' +
                  str(self.color.green()) + ',' + str(self.color.blue()) + '>')
            buffer.append('<'+str(self.mode)+',' + str(self.color.red()) + ',' +
                          str(self.color.green()) + ',' + str(self.color.blue()) + '>')

    def saveColor(self):
        if (self.color.isValid()):
            self.sender().obj.setStyleSheet(
                'background-color: ' + self.color.name(self.color.HexRgb))
            self.saveToRegistry(
                self.sender().obj.objectName(), str(self.color.name()))

    def loadColor(self):
        sender = self.sender()
        self.color = sender.obj.palette().color(QtGui.QPalette.Background)
        self.lColor.setStyleSheet(
            'background-color: ' + self.color.name(self.color.HexRgb))
        self.leColor.setText(self.color.name())
        buffer.append('<'+str(self.mode)+',' + str(self.color.red()) + ',' +
                      str(self.color.green()) + ',' + str(self.color.blue()) + '>')

    def refreshQue(self):
        self.color = QtGui.QColor(self.leColor.text())
        print('<'+str(self.mode)+',' + str(self.color.red()) + ',' +
              str(self.color.green()) + ',' + str(self.color.blue()) + '>')
        buffer.append('<'+str(self.mode)+',' + str(self.color.red()) + ',' +
                      str(self.color.green()) + ',' + str(self.color.blue()) + '>')

    def updateMode(self):
        if (self.rbAnim_PerlinFade.isChecked()):
            self.mode = 1
        if (self.rbAnim_ArrowWaves.isChecked()):
            self.mode = 2


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
