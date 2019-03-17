# -*- coding: UTF-8 -*-

import os
import xlrd
import openpyxl
import time
import sys
import ctypes
import datetime
import threading
import pandas as pd
from windowsmomo import *
from SettingWindow import *
# from Daochu_test import Daochu_shuju
from data_import import Daochu_shuju
from make_pingzheng import Zhizuo_pingzheng
from shengchengguzhibiao import Shengcheng_guzhibiao
from dianziduizhangguanli import Guanli_dianziduizhang
from toucun_baobiaodaochu import Daochu_toucunbaobiao
from jijin_zichanbiaodaochu import Daochu_jijinzichan
from zichan_baobiaodaochu import Daochu_zichanbaobiao
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QFileDialog, QMenu, QAction
from common import send_email_to_admin

ascale = 0.73
a1scale = 0.73
a2scale = 0.95
stepdic = {1: '进行环境检查', 2: '读取产品参数维护表', 3: '启动估值系统', 4: '文件导入', 5: '制作凭证', 6: '生成估值表', 7: '关闭等待托管行', 8: '启动报表系统',
           9: '电子对账查询', 10: '处理并发送对账结果', 11: '关闭等待托管行', 12: '启动报表系统', 13: '导出资产情况统计表', 14: '导出现金头寸预测汇总表', 15: '关闭',
           16: '启动O32', 17: '导出基金资产表', 18: '净值核对', 19: '关闭'}

# -----------------------------------------------------------------------------------------
# 提供给自动化脚本的参数相关
year = str(datetime.datetime.now().year)
month = str(datetime.datetime.now().month)
day = str(datetime.datetime.now().day)

blacklist = []  # 存放用户遇到这些窗口之后就停止的黑名单

email_server_url = "smtp.qq.com"  # 发送邮件的服务器地址
email_server_port = 25  # 发送邮件的服务器端口
sender_email = 'xxx@qq.com'  # 发送邮件的账号
sender_passwd = ''  # 发送者密码
reciever_email = []  # 接收邮件的账号

jijinListTotal = []  # 存放基金总表
jijinListSelected = []  # 存放要选择的基金

dataPath = ''
imPath = ''
exPath = ''
fundName = ''

gzPath = ''
gzName = ''
gzPW = ''
cwPath = ''
cwName = ''
cwPW = ''
o32Path = ''
o32Name = ''
o32PW = ''

catch = 0

flagCir = 1
dictC = {}
confName = ''

threadid = 0
single = 0
cntnDo = 0
F = []
w3 = 0.03


def getConf():
    readconf = open('conf.txt', 'r', encoding='gbk')
    global dictC
    global flag
    for i in readconf.readlines():
        if '：' in i and '*' not in i:
            listC = i[:-1].split('：')
            if listC[0] == '填写人' and listC[1] == '':
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
    global imPath
    global exPath
    global fundName
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

    global w3

    if flag == 1:
        dataPath = dictC['选取基金列表']
        imPath = dictC['导入数据目录']
        exPath = dictC['导出数据目录']
        fundName = dictC['默认基金名称']

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
        tmpr = dictC['接受者邮箱账号列表'].split('、')
        reciever_email = tmpr

        bl = dictC['黑名单']
        if bl != "":
            blacklist = bl.split('、')

        if dataPath != '':
            data = pd.read_excel(dataPath)
            data = pd.DataFrame(data)
            jijinListTotal = list(data['基金'])
            jijinListSelected = list(data['可选基金'])

        w3 = float(dictC['循环间隔时间'])

        return flag
    else:
        return flag


def DaochuShujuThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                      o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                      email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                      jijinListSelected):
    global single
    try:
        Daochu_shuju(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                     o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                     email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal, jijinListSelected, single, cntnDo)
        # Daochu_shuju()
        if single == 0:
            obj.s.step5.emit()
        elif single == 1:
            single = 0
            frame = QImage('image/loadL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.step4Label.width(), obj.step4Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.step4Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('4')
        fwc.close()


def ZhizuoPingzhengThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                          o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                          email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                          jijinListSelected):
    global single
    try:
        Zhizuo_pingzheng(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                         o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                         email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                         jijinListSelected, single, cntnDo)
        # Daochu_shuju()
        if single == 0:
            obj.s.step6.emit()
        elif single == 1:
            single = 0
            frame = QImage('image/makeKeyL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.step5Label.width(), obj.step5Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.step5Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('5')
        fwc.close()


def ShengchengGuzhibiaoThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                              o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                              email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                              jijinListSelected):
    global single
    try:
        Shengcheng_guzhibiao(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                             o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                             email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                             jijinListSelected, single, cntnDo)
        # Daochu_shuju()
        if single == 0:
            obj.s.step7.emit()
        elif single == 1 and 6 not in F:
            single = 0
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.step6Label.width(), obj.step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.step6Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('6')
        fwc.close()


def Guanli_DianziduizhangThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                                o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                                email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                                jijinListSelected):
    global single
    try:
        Guanli_dianziduizhang(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                              o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                              email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                              jijinListSelected)
        # Daochu_shuju()
        if single == 0:
            obj.s.step10.emit()
        elif single == 1:
            single = 1
            frame = QImage('image/mngL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.step9Label.width(), obj.step9Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.step9Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('9')
        fwc.close()


def Daochu_ZichanbaobiaoThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                               o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                               email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                               jijinListSelected):
    global single
    try:
        Daochu_zichanbaobiao(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                             o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                             email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                             jijinListSelected)
        # Daochu_shuju()
        if single == 0:
            obj.s.Tstep3.emit()
        elif single == 1:
            single = 0
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.T2step2Label.width(), obj.T2step2Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.T2step2Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('13')
        fwc.close()


def Daochu_ToucunThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                        o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                        email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                        jijinListSelected):
    global single
    try:
        Daochu_toucunbaobiao(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                             o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                             email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                             jijinListSelected)
        # Daochu_shuju()
        if single == 0:
            obj.s.Tstep4.emit()
        elif single == 1:
            single = 0
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.T2step3Label.width(), obj.T2step3Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.T2step3Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('14')
        fwc.close()


def Daochu_JijinbaobiaoThread(obj, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                              o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                              email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                              jijinListSelected):
    global single
    try:
        Daochu_jijinzichan(dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW,
                           o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url,
                           email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal,
                           jijinListSelected)
        # Daochu_shuju()
        if single == 0:
            obj.s.Tstep7.emit()
        elif single == 1:
            single = 0
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.T2step6Label.width(), obj.T2step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.T2step6Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('17')
        fwc.close()


def hebing_excel(obj, heduijingzhi_excel, toucun_excel, zichan_excel, jijin_excel, outputexcel, email_server_url,
                 email_server_port, sender_email, sender_passwd, reciever_email, exPath, flagCir):
    try:
        from process_excel import Merge_excels
        Merge_excels(heduijingzhi_excel, toucun_excel, zichan_excel, jijin_excel, outputexcel, email_server_url,
                     email_server_port, sender_email, sender_passwd, reciever_email, exPath, flagCir)
        # Daochu_shuju()
        global single
        if single == 0:
            obj.s.Tstep8.emit()
        elif single == 1 and 27 not in F:
            single = 0
            frame = QImage('image/mngL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = obj.T2step7Label.width(), obj.T2step7Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            obj.T2step7Label.setPixmap(pix)
            obj.startButton.setEnabled(True)
            QApplication.processEvents()
    except:
        import traceback
        traceback.print_exc()
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write(sys.exc_info()[0])
        fwc.write(sys.exc_info()[1])
        fwc.close()


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        print('run')
        self.func()


# -----------------------------------------------------------------------------------------
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
    Tstep1 = pyqtSignal()
    Tstep2 = pyqtSignal()
    Tstep3 = pyqtSignal()
    Tstep4 = pyqtSignal()
    Tstep5 = pyqtSignal()
    Tstep6 = pyqtSignal()
    Tstep7 = pyqtSignal()
    Tstep8 = pyqtSignal()
    Twait1 = pyqtSignal()


class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.startUp()

    def startUp(self):
        self.s = Communicate()
        self.min.clicked.connect(self.minFun)
        self.quit.clicked.connect(self.closeFun)
        self.startButton.clicked.connect(self.on_click)
        self.quitButton.clicked.connect(self.quit_click)
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
        # self.arrows2LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.arrows2LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait1)
        # self.arrows7LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.arrows7LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait2)
        # self.arrows11LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.arrows11LongLabel.customContextMenuRequested.connect(self.custom_right_menu_wait3)
        self.T2step2Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.T2step2Label.customContextMenuRequested.connect(self.custom_right_menu_T2s2)
        self.T2step3Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.T2step3Label.customContextMenuRequested.connect(self.custom_right_menu_T2s3)
        self.T2step6Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.T2step6Label.customContextMenuRequested.connect(self.custom_right_menu_T2s6)
        self.T2step7Label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.T2step7Label.customContextMenuRequested.connect(self.custom_right_menu_T2s7)
        # self.T2arrows4LongLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.T2arrows4LongLabel.customContextMenuRequested.connect(self.custom_right_menu_T2w1)

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
        self.s.Tstep1.connect(self.Tstep1Changed)
        self.s.Tstep2.connect(self.Tstep2Changed)
        self.s.Tstep3.connect(self.Tstep3Changed)
        self.s.Tstep4.connect(self.Tstep4Changed)
        self.s.Tstep5.connect(self.Tstep5Changed)
        self.s.Tstep6.connect(self.Tstep6Changed)
        self.s.Tstep7.connect(self.Tstep7Changed)
        self.s.Tstep8.connect(self.Tstep8Changed)
        self.s.Twait1.connect(self.Twait1Changed)
        frc = open('catch.txt', 'r', encoding='utf8')
        c = frc.read()
        if c != '0' and c != '':
            stp = stepdic[int(c)]
            print(stp)
            QMessageBox.information(self, "提示", "上次执行【" + stp + "】出现异常", QMessageBox.Yes)
        frc.close()
        fwc = open('catch.txt', 'w', encoding='utf8')
        fwc.write('0')
        fwc.close()

    def on_click(self):
        t = MyThread(self.threadClick)
        t.start()

    def threadClick(self):
        self.startButton.setEnabled(True)
        QApplication.processEvents()
        setValue()
        global chldt1
        global cntnDo
        if dataPath == '' or imPath == '' or exPath == '' or fundName == '' or gzPath == '' or gzName == '' or gzPW == '' or cwPath == '' or cwName == '' or cwPW == '' or o32Path == '' or o32Name == '' or o32PW == '':
            self.dialog()
        else:
            if self.setTime.isChecked():
                status = True
                while status:
                    print(self.startTimeEdit.text())
                    hour = str(datetime.datetime.now().hour)
                    minute = str(datetime.datetime.now().minute)
                    print(hour, minute)
                    setStart = self.startTimeEdit.text().split(':')
                    if (setStart[0] < hour) or (setStart[0] == hour and setStart[1] <= minute):
                        status = False
                        if self.tabWidget.currentIndex() == 0:
                            cntnDo = 1
                            self.s.step1.emit()
                        else:
                            cntnDo = 1
                            self.s.Tstep1.emit()
                    else:
                        time.sleep(60)
            else:
                if self.tabWidget.currentIndex() == 0:
                    cntnDo = 1
                    self.s.step1.emit()
                else:
                    cntnDo = 1
                    self.s.Tstep1.emit()
        self.startButton.setEnabled(False)
        QApplication.processEvents()

    def pause_click(self):
        if self.PauseButton.text() == '暂停':
            self.PauseButton.setText('继续')
            QApplication.processEvents()
            print('暂停')
        elif self.PauseButton.text() == '继续':
            self.PauseButton.setText('暂停')
            QApplication.processEvents()
            print('继续')

    def quit_click(self):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(threadid, ctypes.py_object(SystemExit))

    def minFun(self):
        self.showMinimized()

    def closeFun(self):
        self.close()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(threadid, ctypes.py_object(SystemExit))

    def getData(self):
        print('1')
        directory, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)

    # def timeDialog(self):
    #     try:
    #         text, ok = QInputDialog.getText(self, '设置等待时间', '请输入等待分钟数:')
    #         if ok:
    #             print(text)
    #             return text
    #     except:
    #         print('error')
    #         return '0'

    def dialog(self):
        QMessageBox.information(self, "提示", "请填写【设置】功能中的必选页面", QMessageBox.Yes)

    def delayDialog(self):
        QMessageBox.information(self, "提示", "不在设定时间范围，稍后程序将准时执行", QMessageBox.Yes)

    def custom_right_menu_step4(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.step4Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/loadF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step4Label.width(), self.step4Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step4Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(4)
        elif action == opt2:
            frame = QImage('image/loadL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step4Label.width(), self.step4Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step4Label.setPixmap(pix)
            QApplication.processEvents()
            if 4 in F:
                F.remove(4)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.step4Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.step4Changed()
        else:
            print('cancel')

    def custom_right_menu_step5(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.step5Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/makeKeyF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step5Label.width(), self.step5Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step5Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(5)
        elif action == opt2:
            frame = QImage('image/makeKeyL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step5Label.width(), self.step5Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step5Label.setPixmap(pix)
            QApplication.processEvents()
            if 5 in F:
                F.remove(5)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.step5Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.step5Changed()
        else:
            print('cancel')

    def custom_right_menu_step6(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.step6Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/productF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step6Label.width(), self.step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step6Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(6)
        elif action == opt2:
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step6Label.width(), self.step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step6Label.setPixmap(pix)
            QApplication.processEvents()
            if 6 in F:
                F.remove(6)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.step6Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.step6Changed()
        else:
            print('cancel')

    def custom_right_menu_step9(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.step9Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/mngF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step9Label.width(), self.step9Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step9Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(9)
        elif action == opt2:
            frame = QImage('image/mngL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step9Label.width(), self.step9Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step9Label.setPixmap(pix)
            QApplication.processEvents()
            if 9 in F:
                F.remove(9)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.step9Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.step9Changed()
        else:
            print('cancel')

    def custom_right_menu_step10(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.step10Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/sendF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step10Label.width(), self.step10Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step10Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(10)
        elif action == opt2:
            frame = QImage('image/sendL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.step10Label.width(), self.step10Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.step10Label.setPixmap(pix)
            QApplication.processEvents()
            if 10 in F:
                F.remove(10)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.step10Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.step10Changed()
        else:
            print('cancel')

    def custom_right_menu_wait1(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows2LongLabel.mapToGlobal(pos))
        global w1
        if action == opt1:
            w1 = self.timeDialog()
            w1 = float(w1)
        else:
            print('2')

    def custom_right_menu_wait2(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows7LongLabel.mapToGlobal(pos))
        global w2
        if action == opt1:
            w2 = self.timeDialog()
            w2 = float(w2)
        else:
            print('2')

    def custom_right_menu_wait3(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.arrows11LongLabel.mapToGlobal(pos))
        global w3
        if action == opt1:
            w3 = self.timeDialog()
            w3 = float(w3)
        else:
            print('2')

    def custom_right_menu_T2w1(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("设置等待时间")
        action = menu.exec_(self.T2arrows4LongLabel.mapToGlobal(pos))
        global tw1
        if action == opt1:
            tw1 = self.timeDialog()
            tw1 = float(tw1)
        else:
            print('2')

    def custom_right_menu_T2s2(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.T2step2Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/productF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step2Label.width(), self.T2step2Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step2Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(22)
        elif action == opt2:
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step2Label.width(), self.T2step2Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step2Label.setPixmap(pix)
            QApplication.processEvents()
            if 22 in F:
                F.remove(22)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.Tstep2Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.Tstep2Changed()
        else:
            print('cancel')

    def custom_right_menu_T2s3(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.T2step3Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/productF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step3Label.width(), self.T2step3Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step3Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(23)
        elif action == opt2:
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step3Label.width(), self.T2step3Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step3Label.setPixmap(pix)
            QApplication.processEvents()
            if 23 in F:
                F.remove(23)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.Tstep3Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.Tstep3Changed()
        else:
            print('cancel')

    def custom_right_menu_T2s6(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.T2step6Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/productF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step6Label.width(), self.T2step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step6Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(26)
        elif action == opt2:
            frame = QImage('image/productL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step6Label.width(), self.T2step6Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step6Label.setPixmap(pix)
            QApplication.processEvents()
            if 26 in F:
                F.remove(26)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.Tstep6Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.Tstep6Changed()
        else:
            print('cancel')

    def custom_right_menu_T2s7(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("禁用")
        opt2 = menu.addAction("启用")
        opt3 = menu.addAction("单步重做")
        opt4 = menu.addAction("继续执行")
        action = menu.exec_(self.T2step7Label.mapToGlobal(pos))
        global single
        global F
        global cntnDo
        if action == opt1:
            frame = QImage('image/mngF.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step7Label.width(), self.T2step7Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step7Label.setPixmap(pix)
            QApplication.processEvents()
            F.append(27)
        elif action == opt2:
            frame = QImage('image/mngL.png')
            imgw, imgh = frame.width(), frame.height()
            lbw, lbh = self.T2step7Label.width(), self.T2step7Label.height()
            rew, reh = int((lbh / imgh) * imgw), int(lbh)
            size = QtCore.QSize(rew, reh)
            pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            self.T2step7Label.setPixmap(pix)
            QApplication.processEvents()
            if 27 in F:
                F.remove(27)
        elif action == opt3:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            single = 1
            self.Tstep7Changed()
        elif action == opt4:
            self.startButton.setEnabled(False)
            QApplication.processEvents()
            cntnDo = 1
            self.Tstep7Changed()
        else:
            print('cancel')

    def step1Changed(self):
        global threadid
        threadid = threading.currentThread().ident
        print('ct', threadid)
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
        try:
            if 4 not in F:
                frame = QImage('image/loadD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step4Label.width(), self.step4Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step4Label.setPixmap(pix)
                QApplication.processEvents()
                print('s4')
                time.sleep(2)
                threading.Thread(target=DaochuShujuThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month, day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 4 in F:
                self.s.step5.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('4')
            fwc.close()

    def step5Changed(self):
        frame = QImage('image/loadL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step4Label.width(), self.step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step4Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 5 not in F:
                frame = QImage('image/makeKeyD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step5Label.width(), self.step5Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step5Label.setPixmap(pix)
                QApplication.processEvents()
                print('s5')
                time.sleep(2)
                threading.Thread(target=ZhizuoPingzhengThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month, day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal, jijinListSelected)).start()
            elif 5 in F:
                self.s.step6.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('9')
            fwc.close()

    def step6Changed(self):
        frame = QImage('image/makeKeyL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step5Label.width(), self.step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step5Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 6 not in F:
                frame = QImage('image/productD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step6Label.width(), self.step6Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step6Label.setPixmap(pix)
                QApplication.processEvents()
                print('s6')
                time.sleep(2)
                threading.Thread(target=ShengchengGuzhibiaoThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month,
                    day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 6 in F:
                self.s.step7.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('6')
            fwc.close()

    def step7Changed(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step6Label.width(), self.step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step6Label.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step7Label.width(), self.step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step7Label.setPixmap(pix)
        QApplication.processEvents()
        print('s7')
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

        frame = QImage('image/arrowsLongD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()
        print('w2')
        time.sleep(2)
        self.s.step8.emit()

    def step8Changed(self):
        s8 = '循环3次，正在执行第' + str(flagCir) + '次'
        self.arrows11Text.setText(s8)
        QApplication.processEvents()

        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows7LongLabel.width(), self.arrows7LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a1scale), int(lbh * a1scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows7LongLabel.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step8Label.width(), self.step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step8Label.setPixmap(pix)
        QApplication.processEvents()
        print('s8')
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
        try:
            if 9 not in F:
                frame = QImage('image/mngD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step9Label.width(), self.step9Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step9Label.setPixmap(pix)
                QApplication.processEvents()
                print('s9')
                time.sleep(2)
                threading.Thread(target=Guanli_DianziduizhangThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month,
                    day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 9 in F:
                self.s.step10.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('9')
            fwc.close()

    def step10Changed(self):
        frame = QImage('image/mngL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step9Label.width(), self.step9Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step9Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            global single
            if single == 0 and 10 not in F:
                frame = QImage('image/sendD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step10Label.width(), self.step10Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step10Label.setPixmap(pix)
                QApplication.processEvents()
                print('s10')
                time.sleep(2)
                send_email_to_admin("helloworld", email_server_url, email_server_port, sender_email, sender_passwd,
                                    reciever_email, exPath + "/对帐结果管理.xls", 1, flagCir)
                self.s.step11.emit()
            elif single == 1 and 10 not in F:
                frame = QImage('image/sendD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step10Label.width(), self.step10Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step10Label.setPixmap(pix)
                QApplication.processEvents()
                print('s10')
                time.sleep(2)
                send_email_to_admin("helloworld", email_server_url, email_server_port, sender_email, sender_passwd,
                                    reciever_email, exPath + "/对帐结果管理.xls", 1, flagCir)
                single = 1
                frame = QImage('image/sendL.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.step10Label.width(), self.step10Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.step10Label.setPixmap(pix)
                QApplication.processEvents()
            elif 10 in F:
                self.s.step11.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('10')
            fwc.close()

    def step11Changed(self):
        frame = QImage('image/sendL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step10Label.width(), self.step10Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step10Label.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.step11Label.width(), self.step11Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.step11Label.setPixmap(pix)
        QApplication.processEvents()
        print('s11')
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

        frame = QImage('image/arrowsLong2D.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.arrows11LongLabel.width(), self.arrows11LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * a2scale), int(lbh * a2scale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.arrows11LongLabel.setPixmap(pix)
        QApplication.processEvents()
        print('w3', w3)
        time.sleep(w3 * 60)
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
        global flagCir
        global cntnDo
        if flagCir <= 2:
            flagCir = flagCir + 1
            self.s.step8.emit()
        else:
            self.arrows11Text.setText('循环3次')
            QApplication.processEvents()
            flagCir = 1
            cntnDo = 0

            cntnDo = 0

            self.startButton.setEnabled(True)
            QApplication.processEvents()
            # self.tabWidget.setCurrentIndex(1)
            # self.s.Tstep1.emit()

    def Tstep1Changed(self):
        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step1Label.width(), self.T2step1Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step1Label.setPixmap(pix)
        QApplication.processEvents()
        print('ts1')
        time.sleep(2)
        self.s.Tstep2.emit()

    def Tstep2Changed(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step1Label.width(), self.T2step1Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step1Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 22 not in F:
                frame = QImage('image/productD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.T2step2Label.width(), self.T2step2Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.T2step2Label.setPixmap(pix)
                QApplication.processEvents()
                print('s2')
                time.sleep(2)
                threading.Thread(target=Daochu_ZichanbaobiaoThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month,
                    day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 22 in F:
                self.s.Tstep3.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('13')
            fwc.close()

    def Tstep3Changed(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step2Label.width(), self.T2step2Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step2Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 23 not in F:
                frame = QImage('image/productD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.T2step3Label.width(), self.T2step3Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.T2step3Label.setPixmap(pix)
                QApplication.processEvents()
                print('w1')
                time.sleep(2)
                threading.Thread(target=Daochu_ToucunThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month,
                    day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 23 in F:
                self.s.Tstep4.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('14')
            fwc.close()

    def Tstep4Changed(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step3Label.width(), self.T2step3Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step3Label.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step4Label.width(), self.T2step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step4Label.setPixmap(pix)
        QApplication.processEvents()
        print('s4')
        time.sleep(2)
        self.s.Twait1.emit()

    def Twait1Changed(self):
        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step4Label.width(), self.T2step4Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step4Label.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/arrowsLongD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2arrows4LongLabel.width(), self.T2arrows4LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * ascale), int(lbh * ascale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2arrows4LongLabel.setPixmap(pix)
        QApplication.processEvents()
        print('w1')
        time.sleep(2)
        self.s.Tstep5.emit()

    def Tstep5Changed(self):
        frame = QImage('image/arrowsLongL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2arrows4LongLabel.width(), self.T2arrows4LongLabel.height()
        rew, reh = int((lbh / imgh) * imgw * ascale), int(lbh * ascale)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2arrows4LongLabel.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/setupD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step5Label.width(), self.T2step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step5Label.setPixmap(pix)
        QApplication.processEvents()
        print('s5')
        time.sleep(2)
        self.s.Tstep6.emit()

    def Tstep6Changed(self):
        frame = QImage('image/setupL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step5Label.width(), self.T2step5Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step5Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 26 not in F:
                frame = QImage('image/productD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.T2step6Label.width(), self.T2step6Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.T2step6Label.setPixmap(pix)
                QApplication.processEvents()
                print('s6')
                time.sleep(2)
                threading.Thread(target=Daochu_JijinbaobiaoThread, args=(
                    self, dataPath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path,
                    o32Name,
                    o32PW, year, month,
                    day,
                    blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email,
                    jijinListTotal,
                    jijinListSelected)).start()
            elif 26 in F:
                self.s.Tstep7.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('17')
            fwc.close()

    def Tstep7Changed(self):
        frame = QImage('image/productL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step6Label.width(), self.T2step6Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step6Label.setPixmap(pix)
        QApplication.processEvents()
        try:
            if 27 not in F:
                frame = QImage('image/mngD.png')
                imgw, imgh = frame.width(), frame.height()
                lbw, lbh = self.T2step7Label.width(), self.T2step7Label.height()
                rew, reh = int((lbh / imgh) * imgw), int(lbh)
                size = QtCore.QSize(rew, reh)
                pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
                self.T2step7Label.setPixmap(pix)
                QApplication.processEvents()
                print('s7')
                time.sleep(2)
                threading.Thread(target=hebing_excel, args=(
                    self, exPath + "\\核对净值示范空表.xlsx", exPath + "\\现金头寸预测汇总表.xls", exPath + "\\资产情况统计表.xls",
                    exPath + "\\综合信息查询_基金资产.xls", exPath + "\\净值核对结果.xlsx", email_server_url, email_server_port,
                    sender_email, sender_passwd, reciever_email, exPath, flagCir)).start()
            elif 27 in F:
                self.s.Tstep8.emit()
        except:
            fwc = open('catch.txt', 'w', encoding='utf8')
            fwc.write('18')
            fwc.close()

    def Tstep8Changed(self):
        frame = QImage('image/mngL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step7Label.width(), self.T2step7Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step7Label.setPixmap(pix)
        QApplication.processEvents()

        frame = QImage('image/quitD.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step8Label.width(), self.T2step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step8Label.setPixmap(pix)
        QApplication.processEvents()
        print('s8')
        time.sleep(2)

        frame = QImage('image/quitL.png')
        imgw, imgh = frame.width(), frame.height()
        lbw, lbh = self.T2step8Label.width(), self.T2step8Label.height()
        rew, reh = int((lbh / imgh) * imgw), int(lbh)
        size = QtCore.QSize(rew, reh)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        self.T2step8Label.setPixmap(pix)
        QApplication.processEvents()
        print('s8')
        time.sleep(2)

        global F
        F = []
        global cntnDo
        cntnDo = 0

        self.startButton.setEnabled(True)
        QApplication.processEvents()


class SettingWindow(QMainWindow, Ui_SettingWindows):
    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.setupUi(self)
        self.startUp()

    def handle_click(self):
        if not self.isVisible():
            self.startUp()
            self.show()

    def startUp(self):
        flag = setValue()
        if flag == 1:
            self.SserverIP.setText(email_server_url)
            self.SserverPort.setText(email_server_port)
            self.SsendID.setText(sender_email)
            self.SsendPW.setText(sender_passwd)
            self.SrsvID.setText('、'.join(reciever_email))

            self.SfilePath.setText(dataPath)
            self.SinPath.setText(imPath)
            self.SoutPath.setText(exPath)
            self.SfundName.setText(fundName)

            self.Ssystem1.setText(gzPath)
            self.SgzName.setText(gzName)
            self.SgzPW.setText(gzPW)
            self.Ssystem2.setText(cwPath)
            self.ScwName.setText(cwName)
            self.ScwPW.setText(cwPW)
            self.Ssystem3.setText(o32Path)
            self.So32Name.setText(o32Name)
            self.So32PW.setText(o32PW)
            self.ScrcTime.setText(str(w3))

            self.SblackList.setText('、'.join(blacklist))

            if year == str(datetime.datetime.now().year) and month == str(datetime.datetime.now().month) and day == str(
                    datetime.datetime.now().day):
                self.Sdate1.setChecked(True)
            elif year == str(datetime.datetime.now().year) and month == str(
                    datetime.datetime.now().month) and day == str(datetime.datetime.now().day - 1):
                self.Sdate2.setChecked(True)
            else:
                self.Sdate3.setChecked(True)
                self.SgetDate.setDate(QDate(int(year), int(month), int(day)))

        self.Scancel.clicked.connect(self.closeFun)
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
        global inPath
        global exPath
        global fundName

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

        global w3

        try:
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

                datelist = datelist.split('-')
                year = datelist[0]
                month = datelist[1]
                day = datelist[2]

            email_server_url = self.SserverIP.text()  # 发送邮件的服务器地址
            email_server_port = self.SserverPort.text()  # 发送邮件的服务器端口
            sender_email = self.SsendID.text()  # 发送邮件的账号
            sender_passwd = self.SsendPW.text()  # 发送者密码
            re = self.SrsvID.toPlainText()  # 接收邮件的账号
            reciever_email = re.split('、')

            dataPath = self.SfilePath.text()
            imPath = self.SinPath.text()
            exPath = self.SoutPath.text()
            fundName = self.SfundName.text()
            gzPath = self.Ssystem1.text()
            gzName = self.SgzName.text()
            gzPW = self.SgzPW.text()
            cwPath = self.Ssystem2.text()
            cwName = self.ScwName.text()
            cwPW = self.ScwPW.text()
            o32Path = self.Ssystem3.text()
            o32Name = self.So32Name.text()
            o32PW = self.So32PW.text()

            w3 = self.ScrcTime.text()

            bl = self.SblackList.toPlainText()
            blacklist = bl.split('、')

            if dataPath == '' or imPath == '' or exPath == '' or fundName == '' or gzPath == '' or gzName == '' or gzPW == '' or cwPath == '' or cwName == '' or cwPW == '' or o32Path == '' or o32Name == '' or o32PW == '':
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
            fwdata = fwdata + '选取基金列表：' + dataPath + '\n'
            fwdata = fwdata + '导入数据目录：' + imPath + '\n'
            fwdata = fwdata + '导出数据目录：' + exPath + '\n'
            fwdata = fwdata + '默认基金名称：' + fundName + '\n\n'
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
            fwdata = fwdata + '接受者邮箱账号列表：' + re + '\n\n'
            fwdata = fwdata + '黑名单：' + bl + '\n\n'
            fwdata = fwdata + '循环间隔时间：' + str(w3) + '\n\n'

            fw.write(fwdata)
            print(fwdata)
            fw.close()
            self.closeFun()
        except:
            QMessageBox.information(self, "提示", "请检查配置文件设置", QMessageBox.Yes)

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

