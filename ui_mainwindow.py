# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Fri Jun  7 17:40:38 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1177, 696)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.devtree = QtWidgets.QTreeWidget(self.centralWidget)
        self.devtree.setGeometry(QtCore.QRect(40, 130, 271, 251))
        self.devtree.setObjectName("devtree")
        item_0 = QtWidgets.QTreeWidgetItem(self.devtree)
        item_0 = QtWidgets.QTreeWidgetItem(self.devtree)
        self.lcd_ph = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcd_ph.setGeometry(QtCore.QRect(800, 130, 221, 121))
        self.lcd_ph.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_ph.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcd_ph.setSmallDecimalPoint(False)
        self.lcd_ph.setDigitCount(4)
        self.lcd_ph.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_ph.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_ph.setProperty("value", 0.0)
        self.lcd_ph.setProperty("intValue", 0)
        self.lcd_ph.setObjectName("lcd_ph")
        self.label_ph = QtWidgets.QLabel(self.centralWidget)
        self.label_ph.setGeometry(QtCore.QRect(620, 130, 131, 121))
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setWeight(50)
        font.setBold(False)
        self.label_ph.setFont(font)
        self.label_ph.setObjectName("label_ph")
        self.label_temp = QtWidgets.QLabel(self.centralWidget)
        self.label_temp.setGeometry(QtCore.QRect(360, 260, 431, 121))
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setWeight(50)
        font.setBold(False)
        self.label_temp.setFont(font)
        self.label_temp.setObjectName("label_temp")
        self.lcd_temp = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcd_temp.setGeometry(QtCore.QRect(800, 260, 221, 121))
        self.lcd_temp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcd_temp.setDigitCount(4)
        self.lcd_temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_temp.setObjectName("lcd_temp")
        self.checkBox_logdata = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_logdata.setGeometry(QtCore.QRect(280, 30, 20, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_logdata.setFont(font)
        self.checkBox_logdata.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_logdata.setText("")
        self.checkBox_logdata.setChecked(False)
        self.checkBox_logdata.setAutoRepeat(False)
        self.checkBox_logdata.setTristate(False)
        self.checkBox_logdata.setObjectName("checkBox_logdata")
        self.pushButton_start = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_start.setGeometry(QtCore.QRect(40, 30, 101, 31))
        self.pushButton_start.setObjectName("pushButton_start")
        self.label_logfilename = QtWidgets.QLabel(self.centralWidget)
        self.label_logfilename.setGeometry(QtCore.QRect(180, 60, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_logfilename.setFont(font)
        self.label_logfilename.setObjectName("label_logfilename")
        self.label_logdata = QtWidgets.QLabel(self.centralWidget)
        self.label_logdata.setGeometry(QtCore.QRect(180, 30, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_logdata.setFont(font)
        self.label_logdata.setObjectName("label_logdata")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(40, 70, 101, 31))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.lineEdit_logfilename = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_logfilename.setGeometry(QtCore.QRect(280, 60, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_logfilename.setFont(font)
        self.lineEdit_logfilename.setObjectName("lineEdit_logfilename")
        self.label_logname = QtWidgets.QLabel(self.centralWidget)
        self.label_logname.setGeometry(QtCore.QRect(430, 20, 47, 13))
        self.label_logname.setObjectName("label_logname")
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.devtree, self.checkBox_logdata)
        MainWindow.setTabOrder(self.checkBox_logdata, self.pushButton_start)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "GKBusNet", None, -1))
        self.devtree.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "Devices", None, -1))
        self.devtree.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "Status", None, -1))
        __sortingEnabled = self.devtree.isSortingEnabled()
        self.devtree.setSortingEnabled(False)
        self.devtree.topLevelItem(0).setText(0, QtWidgets.QApplication.translate("MainWindow", "pH Meter", None, -1))
        self.devtree.topLevelItem(0).setText(1, QtWidgets.QApplication.translate("MainWindow", "Not Connected", None, -1))
        self.devtree.topLevelItem(1).setText(0, QtWidgets.QApplication.translate("MainWindow", "Temp Probe", None, -1))
        self.devtree.topLevelItem(1).setText(1, QtWidgets.QApplication.translate("MainWindow", "Not Connected", None, -1))
        self.devtree.setSortingEnabled(__sortingEnabled)
        self.label_ph.setText(QtWidgets.QApplication.translate("MainWindow", "pH =", None, -1))
        self.label_temp.setText(QtWidgets.QApplication.translate("MainWindow", "Temp [degF] =", None, -1))
        self.pushButton_start.setText(QtWidgets.QApplication.translate("MainWindow", "Start", None, -1))
        self.label_logfilename.setText(QtWidgets.QApplication.translate("MainWindow", "Log File Name:", None, -1))
        self.label_logdata.setText(QtWidgets.QApplication.translate("MainWindow", "Log Data:", None, -1))
        self.pushButton_stop.setText(QtWidgets.QApplication.translate("MainWindow", "Stop", None, -1))
        self.label_logname.setText(QtWidgets.QApplication.translate("MainWindow", "TextLabel", None, -1))

