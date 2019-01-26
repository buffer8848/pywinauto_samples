#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/19
# desc: 登陆模块

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from time import sleep

def process_app_login(app, gzName, gzPW):
    #处理登录
    dlg_login = app["估值系统登录"]
    dlg_login.wait("exists enabled visible ready", 60)
    dlg_login.set_focus()
    dlg_login["Edit2"].set_focus()
    dlg_login["Edit2"].set_text(gzName)
    dlg_login["Edit2"].click() #选中一下才能登陆
    sleep(1)
    dlg_login["Edit3"].set_focus()
    dlg_login["Edit3"].set_text(gzPW)
    dlg_login["登录(&L)"].click()
    sleep(1)
    try:
        app.top_window()["确定"].set_focus()
        app.top_window()["确定"].click()
    except Exception:
        None
    try:
        app.top_window()["否(N)"].set_focus()
        app.top_window()["否(N)"].click()
    except Exception:
        None