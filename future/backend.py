import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets
from ui_mainwindow import Ui_MainWindow
import threading as th
import time
import  device_list as dlt
import csv
import logger as logger
import datetime

debug = True
demo = True

header = ['Time', 'pH', 'Temp', 'Dev 0 Stat', 'Dev 1 Stat']
refresh_delay = 1 #Seconds
logfile = 'mydata.csv'
is_start = True

logger = logger.Logger(filename=logfile, header=header, log_enable=False)       

class Backend():

    def __init__(self):

        self.demo = True
        self.header = ['Time', 'pH', 'Temp', 'Dev 0 Stat', 'Dev 1 Stat']
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
        global t1, t2, t3
        global is_start
        is_start = True
        t1 = th.Thread(target=set_all_data, daemon=True).start()
        t2 = th.Thread(target=dlt.start_all_device_data, daemon=True).start()
        t3 = th.Thread(target=controlloop, daemon=True).start()

    def stop():
        global is_start
        is_start = False #thread 3 is closed after full control loop pass is finished
        for i,x in enumerate(dlt.dev): dlt.dev[i].stop_update() #thread 2 is closed after devices are told to stop getting data
        #t1.join(); t2.join(); t3.join();
        if debug: print('All Threads Stopped')