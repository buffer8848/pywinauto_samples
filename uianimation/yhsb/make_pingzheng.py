#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import timings
from time import sleep

from common import restart_if_app_exist

def Zhizuo_pingzheng(year, month, day):
    exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    restart_if_app_exist(exepath)
    sleep(3)

    app = Application().start(exepath)

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
    ctl_sysnvg = dlg_main["系统功能导航"]
    ctl_sysnvg.ThunderRT6UserControlDC5.click()
    sleep(1)

    #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    send_keys(year)
    send_keys("{RIGHT}")
    send_keys(month)
    send_keys("{RIGHT}")
    send_keys(day)
    sleep(2)

    #进入到数据管理页面
    ctl_treedview = dlg_main["非结转损益"]
    ctl_treedview.check()
    sleep(1)
    dlg_main["制作凭证"].set_focus()
    dlg_main["制作凭证"].click()
    sleep(1)
    status = True
    while status: #判断各种异常的弹框，都点yes
        try:
            try:
                if app["业务凭证管理Dialog"]["凭证制作完毕!"].exists():
                    status = False
            except Exception:
                None
            app.top_window()["是(Y)"].set_focus()
            app.top_window()["是(Y)"].click()
            sleep(1)
        except Exception:
            None

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