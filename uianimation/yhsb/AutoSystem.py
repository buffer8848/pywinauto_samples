# -*- coding: UTF-8 -*-

import os
import sys
import datetime
from data_import import Daochu_shuju
from make_pingzheng import Zhizuo_pingzheng
from shengchengguzhibiao import Shengcheng_guzhibiao
from dianziduizhangguanli import Guanli_dianziduizhang
# from toucun_baobiaodaochu import Daochu_toucunbaobiao
# from zichan_baobiaodaochu import Daochu_zichanbaobiao
from windowsmomo import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QFileDialog, QMenu, QAction

class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.startUp()

    def startUp(self):
        self.setting.clicked.connect(self.settingFun)
        self.min.clicked.connect(self.minFun)
        self.quit.clicked.connect(self.closeFun)
        self.startButton.clicked.connect(self.getData)


    def on_click(self):
        print(self.setTime.isChecked())
        self.s.step1.emit()

    def pause_click(self):
        os.system("pause")

    def settingFun(self):
        pass

    def minFun(self):
        self.showMinimized()

    def closeFun(self):
        self.close()

    def getData(self):
        print('1')
        directory, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/")  # 设置文件扩展名过滤,注意用双分号间隔
        print(directory, filetype)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
