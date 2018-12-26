#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/19
# desc: 登陆模块

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from time import sleep

def process_app_login(app):
    #处理登录
    dlg_login = app["估值系统登录"]
    dlg_login.set_focus()
    dlg_login["Edit3"].set_text("1")
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