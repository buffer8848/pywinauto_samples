# -*- coding: UTF-8 -*-

import os
import time
import sys
import datetime
import threading
import pandas as pd
from windowsmomo import *
from SettingWindow import *
from Daochu_test import Daochu_shuju
from data_import import Daochu_shuju
from make_pingzheng import Zhizuo_pingzheng
from shengchengguzhibiao import Shengcheng_guzhibiao
from dianziduizhangguanli import Guanli_dianziduizhang
from toucun_baobiaodaochu import Daochu_toucunbaobiao
from zichan_baobiaodaochu import Daochu_zichanbaobiao
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QFileDialog, QMenu, QAction

ascale = 0.73
a1scale = 0.7
a2scale = 0.63


#-----------------------------------------------------------------------------------------
#提供给自动化脚本的参数相关
year = str(datetime.datetime.now().year)
month = str(datetime.datetime.now().month)
day = str(datetime.datetime.now().day)

blacklist = [] #存放用户遇到这些窗口之后就停止的黑名单

email_server_url = "smtp.qq.com" #发送邮件的服务器地址
email_server_port = 25 #发送邮件的服务器端口
sender_email = 'xxx@qq.com' #发送邮件的账号
sender_passwd = '' #发送者密码
reciever_email = 'xxx@qq.com' #接收邮件的账号

jijinListTotal = [] #存放基金总表
jijinListSelected = [] #存放要选择的基金

dataPath = ''
filePath = ''
gzPath = ''
gzName = ''
gzPW = ''
cwPath = ''
cwName = ''
cwPW = ''
o32Path = ''
o32Name = ''
o32PW = ''

flag = 0
dictC = {}

confName = ''

def getConf():
    readconf = open('conf.txt', 'r', encoding='gbk')
    global dictC
    global flag
    for i in readconf.readlines():
        if '：' in i and '*' not in i:
            listC = i[:-1].split('：')
            if listC[0] =='填写人' and listC[1] == '':
                print('不用填写了！！！！！')
                flag = 0
                print(flag, dictC)
                return flag, dictC
            flag = 1
            dictC[listC[0]] = listC[1]
    readconf.close()
    print(flag, dictC)
    return flag, dictC

def setValue():
    flag, dictC = getConf()
    global confName

    global email_server_url
    global email_server_port
    global sender_email
    global sender_passwd
    global reciever_email

    global dataPath
    global filePath
    global gzPath
    global gzName
    global gzPW
    global cwPath
    global cwName
    global cwPW
    global o32Path
    global o32Name
    global o32PW

    global year
    global month
    global day

    global blacklist
    global jijinListTotal
    global jijinListSelected

    if flag == 1:
        dataPath = dictC['基金列表存放路径']
        filePath = dictC['导出文件目录']

        gzPath = dictC['估值系统路径']
        gzName = dictC['估值账户']
        gzPW = dictC['估值密码']
        cwPath = dictC['财务系统路径']
        cwName = dictC['财务账户']
        cwPW = dictC['财务密码']
        o32Path = dictC['O32系统路径']
        o32Name = dictC['O32账户']
        o32PW = dictC['O32密码']

        confName = dictC['填写人']

        t1 = dictC['T - 1 日']
        tany = dictC['自定义']

        if t1 == '1':
            day = str(int(day) - 1)
        elif tany == '1':
            t = dictC['自定义日期']
            datelist = t.split('/')
            year = str(datelist[0])
            month = str(datelist[1])
            day = str(datelist[2])

        email_server_url = dictC['发送邮件的服务器地址']
        email_server_port = dictC['发送邮件的服务器端口']
        sender_email = dictC['发送者邮箱账号']
        sender_passwd = dictC['发送者邮箱密码']
        reciever_email = dictC['接受者邮箱账号']

        bl = dictC['黑名单']
        blacklist = bl.split('、')

        if dataPath != '':
            data = pd.read_excel(dataPath)
            data = pd.DataFrame(data)
            jijinListTotal = list(data['基金'])
            jijinListSelected = list(data['可选基金'])

        return flag
    else:
        return flag


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func(dataPath, filePath, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal, jijinListSelected)

class MyThreadw(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func()


class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.liststep = {self.step1D: 1, self.step1L: 1, self.step2D: 1, self.step2L: 1, self.wait1D: 1, self.wait1L: 1,
                         self.step3D: 1, self.step3L: 1,
                         self.step4D: 1, self.step4L: 1, self.step5D: 1, self.step5L: 1, self.step6D: 1, self.step6L: 1,
                         self.step7D: 1, self.step7L: 1, self.wait2D: 1, self.wait2L: 1, self.step8D: 1, self.step8L: 1,
                         self.step9D: 1, self.step9L: 1,
                         self.step10D: 1, self.step10L: 1, self.step11D: 1, self.step11L: 1, self.wait3D: 1,
                         self.wait3L: 1}
        self.startUp()

    def startUp(self):
        self.min.clicked.connect(self.minFun)
        self.quit.clicked.connect(self.closeFun)
        self.startButton.clicked.connect(self.on_click)
        self.PauseButton.clicked.connect(self.pause_click)
        self.quitButton.clicked.connect(self.pause_click)
        self.step2Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.step2Label.customContextMenuRequested.connect(self.custom_right_menu_step2)
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

    def on_click(self):
        setValue()
        if dataPath == '' or filePath == '' or gzPath == '' or gzName == '' or gzPW == '' or cwPath == '' or cwName == '' or cwPW == '' or o32Path == '' or o32Name == '' or o32PW == '' :
            self.dialog()
        else:
            if self.setTime.isChecked():
                print(self.startTimeEdit.text(), self.endTimeEdit.text())
                hour = str(datetime.datetime.now().hour)
                secend = str(datetime.datetime.now().second)
                print(hour, secend)
                setStart = self.startTimeEdit.text().split(':')
                setEnd = self.endTimeEdit.text().split(':')
                if (setStart[0] < hour and setEnd[0] > hour) or (setStart[0] == hour and setStart[1] < secend) or (setEnd[0] == hour and setEnd[1] > secend):
                    self.runStep()
                else:
                    self.timeDialog()
            else:
                self.runStep()

    def runStep(self, liststep):
        for ls in liststep:
            if ls == self.step4D or ls == self.step5D or ls == self.step6D or ls == self.step9D or ls == self.step10D:
                t = MyThread(ls)
                t.start()
                t.pause()
                if ls == self.step4D:
                    t1 = MyThread()
            else:
                t = MyThreadw(ls)
                t.start()


    def pause_click(self):
        os.system("pause")

    def minFun(self):
        self.showMinimized()

    def closeFun(self):
        self.close()

    def getData(self):
        print('1')
        directory, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)

    def timeDialog(self):
        text, ok = QInputDialog.getText(self, '设置等待时间', '请输入等待分钟数:')
        if ok:
            print(text)
            return text

    def dialog(self):
        QMessageBox.information(self, "提示", "请填写【设置】功能中的必选页面", QMessageBox.Yes)

    def timeDialog(self):
        QMessageBox.information(self, "提示", "不在设定时间范围，稍后程序将准时执行", QMessageBox.Yes)

    def custom_right_menu_step2(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置读取数据路径")
        action = menu.exec_(self.step2Label.mapToGlobal(pos))
        if action == opt1:
            self.getData()
        else:
            print('2')

    def custom_right_menu_step4(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("单步重做")
        opt2 = menu.addAction("继续执行")
        opt3 = menu.addAction("禁用")
        action = menu.exec_(self.step4Label.mapToGlobal(pos))
        if action == opt1:
            self.step4Changed()
        elif action == opt2:
            frame = QImage('image/loadF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step4Label.width(), self.step4Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step4Label.setPixmap(pix)
            QApplication.processEvents()
        elif action == opt3:
            self.step4Changed()
        else:
            print('4')

    def custom_right_menu_step5(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("单步重做")
        opt2 = menu.addAction("继续执行")
        opt3 = menu.addAction("禁用")
        action = menu.exec_(self.step5Label.mapToGlobal(pos))
        if action == opt1:
            self.step5Changed()
        elif action == opt2:
            pass
        else:
            print('4')

    def custom_right_menu_step6(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("单步重做")
        opt2 = menu.addAction("继续执行")
        opt3 = menu.addAction("禁用")
        action = menu.exec_(self.step6Label.mapToGlobal(pos))
        if action == opt1:
            self.step6Changed()
        elif action == opt2:
            pass

        else:
            print('4')

    def custom_right_menu_step9(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("单步重做")
        opt2 = menu.addAction("继续执行")
        opt3 = menu.addAction("禁用")
        action = menu.exec_(self.step9Label.mapToGlobal(pos))
        if action == opt1:
            self.step9Changed()
        elif action == opt2:
            pass
        elif action == opt3:
            self.timeDialog()
        else:
            print('4')

    def custom_right_menu_step10(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("单步重做")
        opt2 = menu.addAction("继续执行")
        opt3 = menu.addAction("禁用")
        action = menu.exec_(self.step10Label.mapToGlobal(pos))
        if action == opt1:
            self.step10Changed()
        elif action == opt2:
            pass
        elif action == opt3:
            self.timeDialog()
        else:
            print('4')

    def custom_right_menu_step7(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.step7Label.mapToGlobal(pos))
        if action == opt1:
            self.timeDialog()
        else:
            print('2')

    def custom_right_menu_step11(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.step11Label.mapToGlobal(pos))
        if action == opt1:
            self.timeDialog()
        else:
            print('2')


    def custom_right_menu_wait1(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows2LongLabel.mapToGlobal(pos))
        if action == opt1:
            self.timeDialog()
        else:
            print('2')

    def custom_right_menu_wait2(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows7LongLabel.mapToGlobal(pos))
        if action == opt1:
            self.timeDialog()
        else:
            print('2')

    def custom_right_menu_wait3(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows11LongLabel.mapToGlobal(pos))
        if action == opt1:
            self.timeDialog()
        else:
            print('2')

    def step1D(self):
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

    def step1L(self):
        frame = QImage('image/startL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step1Label.width(), self.step1Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step1Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step2D(self):
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

    def step2L(self):
        frame = QImage('image/readL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step2Label.width(), self.step2Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step2Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def wait1D(self):
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


    def wait1L(self):
        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows2LongLabel.width(), self.arrows2LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * ascale), int(lbh * ascale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows2LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step3D(self):
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

    def step3L(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step3Label.width(), self.step3Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step3Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step4D(self):
        frame = QImage('image/loadD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step4Label.width(), self.step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step4Label.setPixmap(pix)
        QApplication.processEvents()
        print('s4')
        t = MyThread(Daochu_shuju)
        t.start()
        self.s.step5.emit()

    def step4L(self):
        frame = QImage('image/loadL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step4Label.width(), self.step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step4Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step5D(self):
        frame = QImage('image/makeKeyD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step5Label.width(), self.step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step5Label.setPixmap(pix)
        QApplication.processEvents()
        t = MyThread(Zhizuo_pingzheng)
        t.start()

    def step5L(self):
        frame = QImage('image/makeKeyL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step5Label.width(), self.step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step5Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step6D(self):
        frame = QImage('image/productD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step6Label.width(), self.step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step6Label.setPixmap(pix)
        QApplication.processEvents()
        t = MyThread(Shengcheng_guzhibiao)
        t.start()

    def step6L(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step6Label.width(), self.step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step6Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step7D(self):
        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step7Label.width(), self.step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step7Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step7L(self):
        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step7Label.width(), self.step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step7Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def wait2D(self):
        frame = QImage('image/arrowsLongD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def wait2L(self):
        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step8D(self):
        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step8L(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step9D(self):
        frame = QImage('image/mngD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step9Label.width(), self.step9Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step9Label.setPixmap(pix)
        QApplication.processEvents()
        t = MyThread(Guanli_dianziduizhang)
        t.start()

    def step9L(self):
        frame = QImage('image/mngL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step9Label.width(), self.step9Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step9Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step10D(self):
        frame = QImage('image/sendD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step10Label.width(), self.step10Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step10Label.setPixmap(pix)
        QApplication.processEvents()
        t = MyThread(Daochu_zichanbaobiao)
        t.start()
        t1 = MyThread(Daochu_toucunbaobiao)
        t1.start()

    def step10L(self):
        frame = QImage('image/sendL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step10Label.width(), self.step10Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step10Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step11D(self):
        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step11Label.width(), self.step11Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step11Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def step11L(self):
        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step11Label.width(), self.step11Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step11Label.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def wait3D(self):
        frame = QImage('image/arrowsLong2D.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows11LongLabel.width(), self.arrows11LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a2scale), int(lbh * a2scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows11LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)

    def wait3L(self):
        frame = QImage('image/arrowsLong2L.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows11LongLabel.width(), self.arrows11LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a2scale), int(lbh * a2scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows11LongLabel.setPixmap(pix)
        QApplication.processEvents()
        time.sleep(2)


class SettingWindow(QMainWindow, Ui_SettingWindows):
    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.setupUi(self)
        self.startUp()

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def startUp(self):
        flag = setValue()
        if flag == 1:
            self.SserverIP.setText(email_server_url)
            self.SserverPort.setText(email_server_port)
            self.SsendID.setText(sender_email)
            self.SsendPW.setText(sender_passwd)
            self.SrsvID.setText(reciever_email)

            self.SfilePath.setText(dataPath)
            self.SdicPath.setText(filePath)
            self.Ssystem1.setText(gzPath)
            self.SgzName.setText(gzName)
            self.SgzPW.setText(gzPW)
            self.Ssystem2.setText(cwPath)
            self.ScwName.setText(cwName)
            self.ScwPW.setText(cwPW)
            self.Ssystem3.setText(o32Path)
            self.So32Name.setText(o32Name)
            self.So32PW.setText(o32PW)

            self.SblackList.setText('、'.join(blacklist))

            if year == str(datetime.datetime.now().year) and month == str(datetime.datetime.now().month) and day == str(datetime.datetime.now().day):
                self.Sdate1.setChecked(True)
            elif year == str(datetime.datetime.now().year) and month == str(datetime.datetime.now().month) and day == str(datetime.datetime.now().day - 1):
                self.Sdate2.setChecked(True)
            else:
                self.Sdate3.setChecked(True)
                self.SgetDate.setDate(QDate(int(year), int(month), int(day)))

        self.Squit.clicked.connect(self.closeFun)
        self.SgetFile.clicked.connect(self.SgetData)
        self.SgetEx.clicked.connect(self.SgetDic)
        self.SgetGz.clicked.connect(self.getSystem1)
        self.SgetCw.clicked.connect(self.getSystem2)
        self.SgetO32.clicked.connect(self.getSystem3)
        self.Ssubmit.clicked.connect(self.submitFun)
        self.Scancel.clicked.connect(self.closeFun)

    def closeFun(self):
        self.close()

    def SgetData(self):
        directory, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)
        self.SfilePath.setText(directory)
        QApplication.processEvents()

    def SgetDic(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文文件夹", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory)
        self.SdicPath.setText(directory)
        QApplication.processEvents()

    def getSystem1(self):
        directory, filetype = QFileDialog.getOpenFileName(self, "选取系统", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)
        self.Ssystem1.setText(directory)
        QApplication.processEvents()

    def getSystem2(self):
        directory, filetype = QFileDialog.getOpenFileName(self, "选取系统", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)
        self.Ssystem2.setText(directory)
        QApplication.processEvents()

    def getSystem3(self):
        directory, filetype = QFileDialog.getOpenFileName(self, "选取系统", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)
        self.Ssystem3.setText(directory)
        QApplication.processEvents()

    def submitFun(self):
        global email_server_url
        global email_server_port
        global sender_email
        global sender_passwd
        global reciever_email

        global dataPath
        global filePath
        global gzPath
        global gzName
        global gzPW
        global cwPath
        global cwName
        global cwPW
        global o32Path
        global o32Name
        global o32PW

        global year
        global month
        global day

        global blacklist
        global jijinListTotal
        global jijinListSelected

        tf = 0
        if self.Sdate1.isChecked():
            tf = 1
            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().month)
            day = str(datetime.datetime.now().day)
        elif self.Sdate2.isChecked():
            tf = 2
            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().month)
            day = str((datetime.datetime.now().day - 1))
        elif self.Sdate3.isChecked():
            tf = 3
            datelist = self.SgetDate.text()
            datelist = datelist.split('/')
            year = datelist[0]
            month = datelist[1]
            day = datelist[2]
        print(year, month, day)

        email_server_url = self.SserverIP.text()  # 发送邮件的服务器地址
        email_server_port = self.SserverPort.text()  # 发送邮件的服务器端口
        sender_email = self.SsendID.text()  # 发送邮件的账号
        sender_passwd = self.SsendPW.text()  # 发送者密码
        reciever_email = self.SrsvID.text()  # 接收邮件的账号

        dataPath = self.SfilePath.text()
        filePath = self.SdicPath.text()
        gzPath = self.Ssystem1.text()
        gzName = self.SgzName.text()
        gzPW = self.SgzPW.text()
        cwPath = self.Ssystem2.text()
        cwName = self.ScwName.text()
        cwPW = self.ScwPW.text()
        o32Path = self.Ssystem3.text()
        o32Name = self.So32Name.text()
        o32PW = self.So32PW.text()

        bl = self.SblackList.toPlainText()
        blacklist = bl.split('、')

        if dataPath == '' or filePath == '' or gzPath == '' or gzName == '' or gzPW == '' or cwPath == '' or cwName == '' or cwPW == '' or o32Path == '' or o32Name == '' or o32PW == '' :
            self.dialog()
        else:
            data = pd.read_excel(dataPath)
            data = pd.DataFrame(data)
            jijinListTotal = list(data['基金'])
            jijinListSelected = list(data['可选基金'])

        fw = open('conf.txt', 'w', encoding='gbk')
        print('run')
        fwdata = '*----------提示1：填写人一项必填----------*\n*----------提示2：冒号请用中文字符----------*\n*----------提示3：选择制作日期请在选中项后标记“1”，年月日用“/”隔开，结尾不加标点----------*\n*----------提示4：黑名单请用中文字符的顿号隔开，名词间无需换行，结尾不加标点----------*\n\n\n'
        fwdata = fwdata + '填写人：' + confName + '\n\n'
        print(confName)
        fwdata = fwdata + '基金列表存放路径：' + dataPath + '\n'
        fwdata = fwdata + '导出文件目录：' + filePath + '\n\n'
        fwdata = fwdata + '估值系统路径：' + gzPath + '\n'
        fwdata = fwdata + '估值账户：' + gzName + '\n'
        fwdata = fwdata + '估值密码：' + gzPW + '\n'
        fwdata = fwdata + '财务系统路径：' + cwPath + '\n'
        fwdata = fwdata + '财务账户：' + cwName + '\n'
        fwdata = fwdata + '财务密码：' + cwPW + '\n'
        fwdata = fwdata + 'O32系统路径：' + o32Path + '\n'
        fwdata = fwdata + 'O32账户：' + o32Name + '\n'
        fwdata = fwdata + 'O32密码：' + o32PW + '\n\n'
        if tf == 1:
            fwdata = fwdata + 'T 日：1\nT - 1 日：\n自定义：\n自定义日期：\n\n'
        elif tf == 2:
            fwdata = fwdata + 'T 日：\nT - 1 日：1\n自定义：\n自定义日期：\n\n'
        elif tf == 3:
            fwdata = fwdata + 'T 日：\nT - 1 日：\n自定义：1\n'
            fwdata = fwdata + '自定义日期：' + year + '/' + month + '/' + day + '\n\n'
        fwdata = fwdata + '发送邮件的服务器地址：' + email_server_url + '\n'
        fwdata = fwdata + '发送邮件的服务器端口：' + email_server_port + '\n'
        fwdata = fwdata + '发送者邮箱账号：' + sender_email + '\n'
        fwdata = fwdata + '发送者邮箱密码：' + sender_passwd + '\n'
        fwdata = fwdata + '接受者邮箱账号：' + reciever_email + '\n\n'
        fwdata = fwdata + '黑名单：' + bl + '\n\n'

        fw.write(fwdata)
        print(fwdata)
        fw.close()
        self.closeFun()


    def dialog(self):
        QMessageBox.information(self, "提示", "请填写必选页面", QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    scdWin = SettingWindow()
    myWin.setting.clicked.connect(scdWin.handle_click)
    myWin.show()
    sys.exit(app.exec_())
    # getConf()

