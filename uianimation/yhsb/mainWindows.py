# -*- coding: UTF-8 -*-

import os
import time
import sys
import multiprocessing
import threading
from windowsmomo import *
from data_import import Daochu_shuju
from make_pingzheng import Zhizuo_pingzheng
from shengchengguzhibiao import Shengcheng_guzhibiao
from dianziduizhangguanli import Guanli_dianziduizhang
from toucun_baobiaodaochu import Daochu_toucunbaobiao
from zichan_baobiaodaochu import Daochu_zichanbaobiao
from multiprocessing import Process, Lock
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog
from multiprocessing import Pool
import datetime

ascale = 0.73
a1scale = 0.7
a2scale = 0.63
lock = Lock()

year = str(datetime.datetime.now().year)
month = str(datetime.datetime.now().month)
day = str(datetime.datetime.now().day)

#-----------------------------------------------------------------------------------------
def DaochuShujuThread(obj, year, month, day):
    Daochu_shuju(year, month, day)
    obj.s.step5.emit()

def ZhizuoPingzhengThread(obj, year, month, day):
    Zhizuo_pingzheng(year, month, day)
    obj.s.step6.emit()

def ShengchengGuzhibiaoThread(obj, year, month, day):
    Shengcheng_guzhibiao(year, month, day)
    obj.s.step7.emit()

def Guanli_DianziduizhangThread(obj, year, month, day):
    Guanli_dianziduizhang(year, month, day)
    obj.s.step10.emit()

def Daochu_ZichanbaobiaoThread(obj, year, month, day):
    Daochu_zichanbaobiao(year, month, day)

class Communicate(QObject):
    step1 = pyqtSignal()
    step2 = pyqtSignal()
    step3 = pyqtSignal()
    step4 = pyqtSignal()
    step5 = pyqtSignal()
    step6 = pyqtSignal()
    step7 = pyqtSignal()
    step8 = pyqtSignal()
    step9 = pyqtSignal()
    step10 = pyqtSignal()
    step11 = pyqtSignal()
    wait1 = pyqtSignal()
    wait2 = pyqtSignal()
    wait3 = pyqtSignal()
    waittmp = pyqtSignal()

class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.startUp()

    def startUp(self):
        self.s = Communicate()
        self.startButton.clicked.connect(self.on_click)
        self.PauseButton.clicked.connect(self.pause_click)
        self.quitButton.clicked.connect(self.pause_click)
        self.step4Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step4Label.customContextMenuRequested.connect(self.custom_right_menu_step4)
        self.step5Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step5Label.customContextMenuRequested.connect(self.custom_right_menu_step5)
        self.step6Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step6Label.customContextMenuRequested.connect(self.custom_right_menu_step6)
        self.step9Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step9Label.customContextMenuRequested.connect(self.custom_right_menu_step9)
        self.step10Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step10Label.customContextMenuRequested.connect(self.custom_right_menu_step10)
        self.step7Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step7Label.customContextMenuRequested.connect(self.custom_right_menu_step7)
        self.step11Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step11Label.customContextMenuRequested.connect(self.custom_right_menu_step11)
        self.arrows2LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arrows2LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait1)
        self.arrows7LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arrows7LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait2)
        self.arrows11LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arrows11LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait3)
        self.s.step1.connect(self.step1Changed)
        self.s.step2.connect(self.step2Changed)
        self.s.step3.connect(self.step3Changed)
        self.s.step4.connect(self.step4Changed)
        self.s.step5.connect(self.step5Changed)
        self.s.step6.connect(self.step6Changed)
        self.s.step7.connect(self.step7Changed)
        self.s.step8.connect(self.step8Changed)
        self.s.step9.connect(self.step9Changed)
        self.s.step10.connect(self.step10Changed)
        self.s.step11.connect(self.step11Changed)
        self.s.wait1.connect(self.wait1Changed)
        self.s.wait2.connect(self.wait2Changed)
        self.s.wait3.connect(self.wait3Changed)
        self.s.waittmp.connect(self.waitTmpChanged)

    def on_click(self):
        print(self.setTime.isChecked())
        self.s.step1.emit()

    def pause_click(self):
        os.system("pause")

    def custom_right_menu_step4(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("重做")
        opt2 = menu.addAction("禁用")
        opt3 = menu.addAction("设置使用时间")
        action = menu.exec_(self.step4Label.mapToGlobal(pos))
        if action == opt1:
            self.step4Changed()
        elif action == opt2:
            print('2')
        elif action == opt3:
            print('3')
        else:
            print('4')

    def custom_right_menu_step5(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("重做")
        opt2 = menu.addAction("禁用")
        opt3 = menu.addAction("设置使用时间")
        action = menu.exec_(self.step5Label.mapToGlobal(pos))
        if action == opt1:
            self.step5Changed()
        elif action == opt2:
            print('2')
        elif action == opt3:
            print('3')
        else:
            print('4')

    def custom_right_menu_step6(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("重做")
        opt2 = menu.addAction("禁用")
        opt3 = menu.addAction("设置使用时间")
        action = menu.exec_(self.step6Label.mapToGlobal(pos))
        if action == opt1:
            self.step6Changed()
        elif action == opt2:
            print('2')
        elif action == opt3:
            print('3')
        else:
            print('4')

    def custom_right_menu_step9(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("重做")
        opt2 = menu.addAction("禁用")
        opt3 = menu.addAction("设置使用时间")
        action = menu.exec_(self.step9Label.mapToGlobal(pos))
        if action == opt1:
            self.step9Changed()
        elif action == opt2:
            print('2')
        elif action == opt3:
            print('3')
        else:
            print('4')

    def custom_right_menu_step10(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("重做")
        opt2 = menu.addAction("禁用")
        opt3 = menu.addAction("设置使用时间")
        action = menu.exec_(self.step10Label.mapToGlobal(pos))
        if action == opt1:
            self.step10Changed()
        elif action == opt2:
            print('2')
        elif action == opt3:
            print('3')
        else:
            print('4')

    def custom_right_menu_step7(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.step7Label.mapToGlobal(pos))
        if action == opt1:
            print('1')
        else:
            print('2')

    def custom_right_menu_step11(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.step11Label.mapToGlobal(pos))
        if action == opt1:
            print('1')
        else:
            print('2')


    def custom_right_menu_wait1(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows2LongLabel.mapToGlobal(pos))
        if action == opt1:
            print('1')
        else:
            print('2')

    def custom_right_menu_wait2(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows7LongLabel.mapToGlobal(pos))
        if action == opt1:
            print('1')
        else:
            print('2')

    def custom_right_menu_wait3(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows11LongLabel.mapToGlobal(pos))
        if action == opt1:
            print('1')
        else:
            print('2')

    def step1Changed(self):
        frame = QImage('image/startD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step1Label.width(), self.step1Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step1Label.setPixmap(pix)
        QApplication.processEvents()
        print('s1')
        time.sleep(2)
        self.s.step2.emit()

    def step2Changed(self):
        frame = QImage('image/startL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step1Label.width(), self.step1Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step1Label.setPixmap(pix)
        QApplication.processEvents()

        time.sleep(2)

        frame = QImage('image/readD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step2Label.width(), self.step2Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step2Label.setPixmap(pix)
        QApplication.processEvents()
        print('s2')
        time.sleep(2)
        self.s.wait1.emit()

    def wait1Changed(self):
        frame = QImage('image/readL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step2Label.width(), self.step2Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step2Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/arrowsLongD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows2LongLabel.width(), self.arrows2LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * ascale), int(lbh * ascale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows2LongLabel.setPixmap(pix)
        QApplication.processEvents()
        print('w1')
        time.sleep(2)
        self.s.step3.emit()

    def step3Changed(self):
        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows2LongLabel.width(), self.arrows2LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * ascale), int(lbh * ascale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows2LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step3Label.width(), self.step3Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step3Label.setPixmap(pix)
        QApplication.processEvents()
        print('s3')
        time.sleep(2)
        self.s.step4.emit()

    def step4Changed(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step3Label.width(), self.step3Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step3Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/loadD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step4Label.width(), self.step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step4Label.setPixmap(pix)
        QApplication.processEvents()
        print('s4')
        threading.Thread(target=DaochuShujuThread, args=(self, year, month, day)).start()
        #pool = Pool(processes=1)
        #pool.apply_async(func=Daochu_shuju, args=(year, month, day), callback=lambda x: self.s.step5.emit())
        #pool.close()

    def step5Changed(self):
        frame = QImage('image/loadL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step4Label.width(), self.step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step4Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/makeKeyD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step5Label.width(), self.step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step5Label.setPixmap(pix)
        QApplication.processEvents()
        threading.Thread(target=ZhizuoPingzhengThread, args=(self, year, month, day)).start()
        #pool = Pool(processes=1)
        #pool.apply_async(func=Zhizuo_pingzheng, args=(year, month, day), callback=lambda x: self.s.step6.emit())
        #pool.close()

    def step6Changed(self):
        frame = QImage('image/makeKeyL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step5Label.width(), self.step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step5Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/productD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step6Label.width(), self.step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step6Label.setPixmap(pix)
        QApplication.processEvents()
        threading.Thread(target=ShengchengGuzhibiaoThread, args=(self, year, month, day)).start()
        #pool = Pool(processes=1)
        #pool.apply_async(func=Shengcheng_guzhibiao, args=(year, month, day), callback=lambda x: self.s.step7.emit())
        #pool.close()

    def step7Changed(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step6Label.width(), self.step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step6Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step7Label.width(), self.step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step7Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.wait2.emit()

    def wait2Changed(self):
        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step7Label.width(), self.step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step7Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/arrowsLongD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.step8.emit()

    def step8Changed(self):
        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.step9.emit()

    def step9Changed(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/mngD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step9Label.width(), self.step9Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step9Label.setPixmap(pix)
        QApplication.processEvents()
        threading.Thread(target=Guanli_DianziduizhangThread, args=(self, year, month, day)).start()
        #pool = Pool(processes=1)
        #pool.apply_async(func=Guanli_dianziduizhang, args=(year, month, day), callback=lambda x: self.s.step10.emit())
        #pool.close()

    def step10Changed(self):
        frame = QImage('image/mngL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step9Label.width(), self.step9Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step9Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/sendD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step10Label.width(), self.step10Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step10Label.setPixmap(pix)
        QApplication.processEvents()
        threading.Thread(target=Daochu_ZichanbaobiaoThread, args=(self, year, month, day)).start()
        #pool = Pool(processes=1)
        #self.pool.apply_async(func=Daochu_zichanbaobiao, args=(year, month, day))
        #pool.close()

    def step11Changed(self):
        frame = QImage('image/sendL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step10Label.width(), self.step10Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step10Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step11Label.width(), self.step11Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step11Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.wait3.emit()

    def wait3Changed(self):
        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step11Label.width(), self.step11Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step11Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/arrowsLong2D.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows11LongLabel.width(), self.arrows11LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a2scale), int(lbh * a2scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows11LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.waittmp.emit()

    def waitTmpChanged(self):
        frame = QImage('image/arrowsLong2L.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows11LongLabel.width(), self.arrows11LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a2scale), int(lbh * a2scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows11LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)
        self.s.step9.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

