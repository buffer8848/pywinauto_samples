# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingWindows(object):
    def setupUi(self, SettingWindows):
        SettingWindows.setObjectName("SettingWindows")
        SettingWindows.resize(864, 581)
        self.centralwidget = QtWidgets.QWidget(SettingWindows)
        SettingWindows.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

        self.centralwidget.setObjectName("centralwidget")
        self.settingTab = QtWidgets.QTabWidget(self.centralwidget)
        self.settingTab.setGeometry(QtCore.QRect(30, 50, 801, 431))
        self.settingTab.setObjectName("settingTab")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.Ssystem2 = QtWidgets.QLineEdit(self.tab1)
        self.Ssystem2.setGeometry(QtCore.QRect(98, 250, 561, 21))
        self.Ssystem2.setObjectName("Ssystem2")
        self.label_5 = QtWidgets.QLabel(self.tab1)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 101, 16))
        self.label_5.setObjectName("label_5")
        self.SgetCw = QtWidgets.QPushButton(self.tab1)
        self.SgetCw.setGeometry(QtCore.QRect(680, 250, 81, 21))
        self.SgetCw.setObjectName("SgetCw")
        self.SgetFile = QtWidgets.QPushButton(self.tab1)
        self.SgetFile.setGeometry(QtCore.QRect(680, 30, 81, 21))
        self.SgetFile.setObjectName("SgetFile")
        self.SfilePath = QtWidgets.QLineEdit(self.tab1)
        self.SfilePath.setGeometry(QtCore.QRect(130, 30, 531, 21))
        self.SfilePath.setObjectName("SfilePath")
        self.Ssystem1 = QtWidgets.QLineEdit(self.tab1)
        self.Ssystem1.setGeometry(QtCore.QRect(100, 170, 561, 21))
        self.Ssystem1.setObjectName("Ssystem1")
        self.label_3 = QtWidgets.QLabel(self.tab1)
        self.label_3.setGeometry(QtCore.QRect(20, 250, 72, 15))
        self.label_3.setObjectName("label_3")
        self.SgetO32 = QtWidgets.QPushButton(self.tab1)
        self.SgetO32.setGeometry(QtCore.QRect(680, 330, 81, 21))
        self.SgetO32.setObjectName("SgetO32")
        self.Ssystem3 = QtWidgets.QLineEdit(self.tab1)
        self.Ssystem3.setGeometry(QtCore.QRect(68, 330, 591, 21))
        self.Ssystem3.setObjectName("Ssystem3")
        self.label_4 = QtWidgets.QLabel(self.tab1)
        self.label_4.setGeometry(QtCore.QRect(20, 330, 72, 15))
        self.label_4.setObjectName("label_4")
        self.SgetGz = QtWidgets.QPushButton(self.tab1)
        self.SgetGz.setGeometry(QtCore.QRect(682, 170, 81, 21))
        self.SgetGz.setObjectName("SgetGz")
        self.label_2 = QtWidgets.QLabel(self.tab1)
        self.label_2.setGeometry(QtCore.QRect(20, 170, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.tab1)
        self.label_6.setGeometry(QtCore.QRect(120, 200, 61, 16))
        self.label_6.setObjectName("label_6")
        self.SgzName = QtWidgets.QLineEdit(self.tab1)
        self.SgzName.setGeometry(QtCore.QRect(180, 200, 161, 21))
        self.SgzName.setObjectName("SgzName")
        self.label_7 = QtWidgets.QLabel(self.tab1)
        self.label_7.setGeometry(QtCore.QRect(380, 200, 41, 16))
        self.label_7.setObjectName("label_7")
        self.SgzPW = QtWidgets.QLineEdit(self.tab1)
        self.SgzPW.setGeometry(QtCore.QRect(430, 200, 161, 21))
        self.SgzPW.setObjectName("SgzPW")
        self.SgzPW.setEchoMode(QLineEdit.Password)
        self.ScwPW = QtWidgets.QLineEdit(self.tab1)
        self.ScwPW.setGeometry(QtCore.QRect(430, 280, 161, 21))
        self.ScwPW.setObjectName("ScwPW")
        self.ScwPW.setEchoMode(QLineEdit.Password)
        self.ScwName = QtWidgets.QLineEdit(self.tab1)
        self.ScwName.setGeometry(QtCore.QRect(180, 280, 161, 21))
        self.ScwName.setObjectName("ScwName")
        self.label_8 = QtWidgets.QLabel(self.tab1)
        self.label_8.setGeometry(QtCore.QRect(380, 280, 41, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab1)
        self.label_9.setGeometry(QtCore.QRect(120, 280, 61, 16))
        self.label_9.setObjectName("label_9")
        self.So32PW = QtWidgets.QLineEdit(self.tab1)
        self.So32PW.setGeometry(QtCore.QRect(430, 360, 161, 21))
        self.So32PW.setObjectName("So32PW")
        self.So32PW.setEchoMode(QLineEdit.Password)
        self.label_10 = QtWidgets.QLabel(self.tab1)
        self.label_10.setGeometry(QtCore.QRect(380, 360, 41, 16))
        self.label_10.setObjectName("label_10")
        self.So32Name = QtWidgets.QLineEdit(self.tab1)
        self.So32Name.setGeometry(QtCore.QRect(180, 360, 161, 21))
        self.So32Name.setObjectName("So32Name")
        self.label_11 = QtWidgets.QLabel(self.tab1)
        self.label_11.setGeometry(QtCore.QRect(120, 360, 61, 16))
        self.label_11.setObjectName("label_11")
        self.SinPath = QtWidgets.QLineEdit(self.tab1)
        self.SinPath.setGeometry(QtCore.QRect(130, 60, 531, 21))
        self.SinPath.setObjectName("SinPath")
        self.label_18 = QtWidgets.QLabel(self.tab1)
        self.label_18.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.label_18.setObjectName("label_18")
        self.SgetIm = QtWidgets.QPushButton(self.tab1)
        self.SgetIm.setGeometry(QtCore.QRect(680, 60, 81, 21))
        self.SgetIm.setObjectName("SgetIm")
        self.SgetEx = QtWidgets.QPushButton(self.tab1)
        self.SgetEx.setGeometry(QtCore.QRect(680, 90, 81, 21))
        self.SgetEx.setObjectName("SgetEx")
        self.SoutPath = QtWidgets.QLineEdit(self.tab1)
        self.SoutPath.setGeometry(QtCore.QRect(130, 90, 531, 21))
        self.SoutPath.setObjectName("SoutPath")
        self.label_19 = QtWidgets.QLabel(self.tab1)
        self.label_19.setGeometry(QtCore.QRect(20, 90, 101, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.tab1)
        self.label_20.setGeometry(QtCore.QRect(20, 120, 101, 16))
        self.label_20.setObjectName("label_20")
        self.SfundName = QtWidgets.QLineEdit(self.tab1)
        self.SfundName.setGeometry(QtCore.QRect(130, 120, 531, 21))
        self.SfundName.setObjectName("SfundName")
        self.settingTab.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.Sdate1 = QtWidgets.QRadioButton(self.tab2)
        self.Sdate1.setGeometry(QtCore.QRect(80, 80, 115, 19))
        self.Sdate1.setChecked(True)
        self.Sdate1.setObjectName("Sdate1")
        self.Sdate2 = QtWidgets.QRadioButton(self.tab2)
        self.Sdate2.setGeometry(QtCore.QRect(80, 140, 115, 19))
        self.Sdate2.setObjectName("Sdate2")
        self.Sdate3 = QtWidgets.QRadioButton(self.tab2)
        self.Sdate3.setGeometry(QtCore.QRect(80, 200, 115, 19))
        self.Sdate3.setObjectName("Sdate3")
        self.SgetDate = QtWidgets.QDateEdit(self.tab2)
        self.SgetDate.setGeometry(QtCore.QRect(170, 200, 110, 22))
        self.SgetDate.setObjectName("SgetDate")
        self.settingTab.addTab(self.tab2, "")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.SserverIP = QtWidgets.QLineEdit(self.tab3)
        self.SserverIP.setGeometry(QtCore.QRect(290, 50, 331, 21))
        self.SserverIP.setObjectName("SserverIP")
        self.label_12 = QtWidgets.QLabel(self.tab3)
        self.label_12.setGeometry(QtCore.QRect(140, 50, 141, 16))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.tab3)
        self.label_14.setGeometry(QtCore.QRect(140, 90, 141, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab3)
        self.label_15.setGeometry(QtCore.QRect(140, 130, 121, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab3)
        self.label_16.setGeometry(QtCore.QRect(140, 170, 101, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab3)
        self.label_17.setGeometry(QtCore.QRect(140, 220, 391, 16))
        self.label_17.setObjectName("label_17")
        self.SserverPort = QtWidgets.QLineEdit(self.tab3)
        self.SserverPort.setGeometry(QtCore.QRect(290, 90, 81, 21))
        self.SserverPort.setObjectName("SserverPort")
        self.SsendID = QtWidgets.QLineEdit(self.tab3)
        self.SsendID.setGeometry(QtCore.QRect(290, 130, 331, 21))
        self.SsendID.setObjectName("SsendID")
        self.SsendPW = QtWidgets.QLineEdit(self.tab3)
        self.SsendPW.setGeometry(QtCore.QRect(290, 170, 331, 21))
        self.SsendPW.setObjectName("SsendPW")
        self.SsendPW.setEchoMode(QLineEdit.Password)
        self.SrsvID = QtWidgets.QTextEdit(self.tab3)
        self.SrsvID.setEnabled(True)
        self.SrsvID.setGeometry(QtCore.QRect(140, 250, 481, 101))
        self.SrsvID.setObjectName("SrsvID")
        self.settingTab.addTab(self.tab3, "")
        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab4")
        self.SblackList = QtWidgets.QTextEdit(self.tab4)
        self.SblackList.setGeometry(QtCore.QRect(50, 110, 681, 221))
        self.SblackList.setObjectName("SblackList")
        self.label_13 = QtWidgets.QLabel(self.tab4)
        self.label_13.setGeometry(QtCore.QRect(20, 30, 351, 51))
        self.label_13.setObjectName("label_13")
        self.settingTab.addTab(self.tab4, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setGeometry(QtCore.QRect(120, 140, 111, 16))
        self.label_21.setObjectName("label_21")
        self.ScrcTime = QtWidgets.QLineEdit(self.tab)
        self.ScrcTime.setGeometry(QtCore.QRect(250, 140, 121, 21))
        self.ScrcTime.setObjectName("ScrcTime")
        self.settingTab.addTab(self.tab, "")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 41, 16))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Ssubmit = QtWidgets.QPushButton(self.centralwidget)
        self.Ssubmit.setGeometry(QtCore.QRect(580, 500, 93, 28))
        self.Ssubmit.setObjectName("Ssubmit")
        self.Scancel = QtWidgets.QPushButton(self.centralwidget)
        self.Scancel.setGeometry(QtCore.QRect(710, 500, 93, 28))
        self.Scancel.setObjectName("Scancel")
        SettingWindows.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingWindows)
        self.settingTab.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(SettingWindows)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)

    def retranslateUi(self, SettingWindows):
        _translate = QtCore.QCoreApplication.translate
        SettingWindows.setWindowTitle(_translate("SettingWindows", "设置"))
        self.label_5.setText(_translate("SettingWindows", "选取基金列表："))
        self.SgetCw.setText(_translate("SettingWindows", "选择系统"))
        self.SgetFile.setText(_translate("SettingWindows", "选择文件"))
        self.label_3.setText(_translate("SettingWindows", "财务系统："))
        self.SgetO32.setText(_translate("SettingWindows", "选择系统"))
        self.label_4.setText(_translate("SettingWindows", "O32："))
        self.SgetGz.setText(_translate("SettingWindows", "选择系统"))
        self.label_2.setText(_translate("SettingWindows", "估值系统："))
        self.label_6.setText(_translate("SettingWindows", "用户名："))
        self.label_7.setText(_translate("SettingWindows", "密码："))
        self.label_8.setText(_translate("SettingWindows", "密码："))
        self.label_9.setText(_translate("SettingWindows", "用户名："))
        self.label_10.setText(_translate("SettingWindows", "密码："))
        self.label_11.setText(_translate("SettingWindows", "用户名："))
        self.label_18.setText(_translate("SettingWindows", "导入数据路径："))
        self.SgetIm.setText(_translate("SettingWindows", "选择文件夹"))
        self.SgetEx.setText(_translate("SettingWindows", "选择文件夹"))
        self.label_19.setText(_translate("SettingWindows", "导出数据路径："))
        self.label_20.setText(_translate("SettingWindows", "默认基金名称："))
        self.settingTab.setTabText(self.settingTab.indexOf(self.tab1), _translate("SettingWindows", "路径（必填）"))
        self.Sdate1.setText(_translate("SettingWindows", " T 日"))
        self.Sdate2.setText(_translate("SettingWindows", " T - 1 日"))
        self.Sdate3.setText(_translate("SettingWindows", " 自定义"))
        self.settingTab.setTabText(self.settingTab.indexOf(self.tab2), _translate("SettingWindows", "制作日期"))
        self.label_12.setText(_translate("SettingWindows", "邮件服务器地址："))
        self.label_14.setText(_translate("SettingWindows", "邮件服务器端口："))
        self.label_15.setText(_translate("SettingWindows", "发送邮箱账号："))
        self.label_16.setText(_translate("SettingWindows", "发送邮箱密码："))
        self.label_17.setText(_translate("SettingWindows", "接收邮箱账号列表（以中文字符“、”分割，无需换行）："))
        self.settingTab.setTabText(self.settingTab.indexOf(self.tab3), _translate("SettingWindows", "邮件"))
        self.label_13.setText(_translate("SettingWindows", "制作黑名单（以中文字符“、”分割，无需换行）："))
        self.settingTab.setTabText(self.settingTab.indexOf(self.tab4), _translate("SettingWindows", "黑名单"))
        self.label_21.setText(_translate("SettingWindows", "循环间隔时间："))
        self.settingTab.setTabText(self.settingTab.indexOf(self.tab), _translate("SettingWindows", "循环间隔时间"))
        self.label.setText(_translate("SettingWindows", "设置"))
        self.Ssubmit.setText(_translate("SettingWindows", "确 定"))
        self.Scancel.setText(_translate("SettingWindows", "取 消"))

