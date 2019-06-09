# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets
from ui_mainwindow import Ui_MainWindow
import threading as th
import time
import device_list as dlt
import csv
import logger as logger
import datetime

'''
Notes:
    Can't use sleep here becuase Qt needs to return to main window to
    re-display changes

    Current Demo Build Run: will display pseudo pH data once connected
                       Temp device has testfail=True, so it will wait
                       10 seconds then raise a custom timeout exception.
                       That stops the get_loop, sets reg1="err", and 
                       status='ConnectionFailed'
    Stats: Current Build at V1.4 can log (5) paramters at 22Hz thats 45ms of delay
'''
debug = True
demo = True
demodata = [1,2,3,4]
header = ['Time', 'pH', 'Temp', 'Dev 0 Stat', 'Dev 1 Stat']
refresh_delay = 1.5 #Seconds
logfile = 'datafiles/mydata.csv'
is_start = True
is_running = False

logger = logger.Logger(filename=logfile, header=header, log_enable=False)

def startup():
    #Update UI elements that depend on backend values and vice versa
    window.ui.lineEdit_logfilename.setText(logger.filename)
    toggle_log()
    print()

def change_logfile():
    logger.filename = window.ui.lineEdit_logfilename.text()
    if debug: print('changed logfilename to {}'.format(logger.filename))

def set_filename_readonly(bool):
    window.ui.lineEdit_logfilename.setReadOnly(bool)

def toggle_log():
    logger.log_enable = window.ui.checkBox_logdata.isChecked()
    if logger.log_enable == False or is_running == False: set_filename_readonly(False)
    else: set_filename_readonly(True)
    if debug: print('logger.log_enable={}'.format(logger.log_enable))

def set_all_data():
    window.ui.devtree.topLevelItem(0).setText(1, dlt.dev[0].status)
    window.ui.lcd_ph.display(dlt.dev[0].reg1)
    window.ui.devtree.topLevelItem(1).setText(1, dlt.dev[1].status)
    window.ui.lcd_temp.display(dlt.dev[1].reg1)

def supervise(): pass

def controlloop():
    if demo: time.sleep(2)
    global is_start
    while is_start:
        logger.log([dlt.dev[0].reg1, dlt.dev[1].reg1, dlt.dev[0].status, dlt.dev[1].status])
        set_all_data()
        supervise()
        time.sleep(refresh_delay)

def start():
    global t1, t2, t3, is_start, is_running
    is_start = True
    if not is_running:
        is_running = True
        t1 = th.Thread(target=set_all_data, daemon=True)
        t2 = th.Thread(target=dlt.start_all_device_data, daemon=True)
        t3 = th.Thread(target=controlloop, daemon=True)
        t1.start(); t2.start(); t3.start()
    else: pass

def stop():
    global t1, t2, t3, is_start, is_running
    is_start = False #thread 3 is closed after full control loop pass is finished
    if is_running:
        set_filename_readonly(False)
        for i,x in enumerate(dlt.dev): dlt.dev[i].stop_update() #thread 2 is closed after devices are told to stop getting data
        t1.join(); t2.join(); t3.join();
        is_running = False
        if debug: print('All Threads Stopped')


class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #add additional links - alternativly I could just pass a value to ui_mainwindow scope
        #and set it there

        QtCore.QObject.connect(self.ui.pushButton_start, QtCore.SIGNAL("clicked()"), start)
        QtCore.QObject.connect(self.ui.pushButton_stop, QtCore.SIGNAL("clicked()"), stop)
        QtCore.QObject.connect(self.ui.lineEdit_logfilename, QtCore.SIGNAL("textEdited(QString)"), change_logfile)
        QtCore.QObject.connect(self.ui.checkBox_logdata, QtCore.SIGNAL("stateChanged(int)"), toggle_log)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    startup()
    # Stars the control program
    #th.Thread(target=builduidevices)
    # app.exec_() runs Qt mainloop
    sys.exit(app.exec_())
    input()