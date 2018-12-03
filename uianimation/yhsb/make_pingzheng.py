#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto import timings
from time import sleep

app = Application().start(r"C:\Program Files\赢时胜资产财务估值系统V2.5\YssGz.exe")

#处理登录
dlg_login = app["估值系统登录"]
dlg_login["Edit3"].set_text("1")
dlg_login["登录(&L)"].click()
sleep(1)
try:
    app.top_window()["否(N)"].set_focus()
    app.top_window()["否(N)"].click()
except Exception:
    None
sleep(1)

#打开数据管理
dlg_main = app["ThunderRT6MDIForm"]
ctl_sysnvg = dlg_main["系统功能导航"]
ctl_sysnvg.ThunderRT6UserControlDC5.click()
sleep(1)

#进入到数据管理页面
ctl_treedview = dlg_main["非结转损益"]
ctl_treedview.check()
sleep(1)
dlg_main["制作凭证"].set_focus()
dlg_main["制作凭证"].click()
sleep(1)
try:
    app.top_window()["是(Y)"].set_focus()
    app.top_window()["是(Y)"].click()
except Exception:
    None

app["业务凭证管理"].wait('ready')
try:
    app.top_window()["确定"].set_focus()
    app.top_window()["确定"].click()
except Exception:
    None

#退出

try:
    dlg_main.close()
except timings.TimeoutError:
    app.top_window()["是(Y)"].click()

#dlg_login.print_control_identifiers()