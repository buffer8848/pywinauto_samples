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

app = Application(backend="win32").start(r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe")

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
sleep(1)

#打开数据管理
dlg_main = app["ThunderRT6MDIForm"]
dlg_main.set_focus()
ctl_sysnvg = dlg_main["系统功能导航"]
ctl_sysnvg.ThunderRT6UserControlDC6.click()
sleep(1)

#进入到数据管理页面
ctl_treedview = dlg_main["TreeView20WndClass2"]
ctl_treedview.set_focus()
ctl_treedview.click(coords=(60, 80))
sleep(1)
dlg_main["读取数据"].set_focus()
dlg_main["读取数据"].click()
sleep(1)
try:
    app["提示信息"]["是(Y)"].click()
except Exception:
    None
sleep(1)
app.top_window()["确定"].click()
sleep(1)

#退出
try:
    dlg_main.close()
except timings.TimeoutError:
    app.top_window()["是(Y)"].click()

#dlg_login.print_control_identifiers()