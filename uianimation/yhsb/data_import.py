#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import mouse
from pywinauto import timings
from time import sleep
#import pytesseract
#import pyautogui as auto
from common import restart_if_app_exist
from common import get_position_of_jijin_list
#import getContent as gd

def Daochu_shuju(year, month, day):
    exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    restart_if_app_exist(exepath)
    sleep(3)
    app = Application(backend="win32").start(exepath)

    #处理登录
    dlg_login = app["估值系统登录"]
    dlg_login.set_focus()
    dlg_login["Edit3"].set_text("1")
    dlg_login["登录(&L)"].click()
    sleep(1)
    try:
        app.top_window()["否(N)"].set_focus()
        app.top_window()["否(N)"].click()
    except Exception:
        None
    sleep(3)

    #打开数据管理
    dlg_main = app["ThunderRT6MDIForm"]
    dlg_main.set_focus()
    ctl_sysnvg = dlg_main["系统功能导航"]
    ctl_sysnvg.ThunderRT6UserControlDC6.click()
    sleep(3)

    # #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    SendKeys("{ENTER}")
    sleep(2)

    #输入文件路径
    dlg_main["按时间段读取Edit2"].set_text(r'C:\估值相关测试数据\QS\QS101' + '\\qw')

    #进入到数据管理页面
    ctl_treedview = dlg_main["TreeView20WndClass"]
    ctl_treedview.set_focus()
    # SendKeys("{LEFT}")
    # gd.getCtn1()

    # 选择基金
    list = ["A003_银华保本增值混合", "A004_银华-道琼斯88指数", "A005_银华货币", "A006_银华价值优选股票", "A002_银华优势企业混合"]
    dict = get_position_of_jijin_list(list, [103, 385], 15)
    for (k, v) in dict.items():
        dlg_main["TreeView20WndClass1"].set_focus()
        mouse.click(coords=(v[0], v[1]))
        sleep(1)

    ctl_treedview = dlg_main["TreeView20WndClass2"]
    ctl_treedview.set_focus()
    ctl_treedview.click(coords=(60, 80))
    sleep(1)
    dlg_main["读取数据"].set_focus()
    dlg_main["读取数据"].click()
    sleep(1)
    while True: #等待保存成功后的弹窗
        try:
            try:
                if app["数据接口管理Dialog"]["读取完毕"].exists():
                    app["数据接口管理Dialog"].set_focus()
                    app["数据接口管理Dialog"]["确定"].click()
                    break
            except Exception:
                None
            app.top_window()["是(Y)"].set_focus()
            app.top_window()["是(Y)"].click()
            sleep(1)
        except Exception:
            None

    #退出
    try:
        dlg_main.close()
    except timings.TimeoutError:
        app.top_window()["是(Y)"].click()

#dlg_login.print_control_identifiers()

#dlg_login.print_control_identifiers()
if __name__ == '__main__':
    Daochu_shuju("2018", "12", "13")