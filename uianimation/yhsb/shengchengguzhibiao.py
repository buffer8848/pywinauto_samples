#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/04
# desc: 生成估值表
#--------------------------------------------------------------------------------------------------

from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import timings
from time import sleep

from common import *

def Shengcheng_guzhibiao(year, month, day):
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
    ctl_sysnvg = dlg_main["msvb_lib_toolbar"]
    ctl_sysnvg.click(coords=(415,15))
    sleep(1)

    #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    sleep(2)

    #勾选生成估值余额对账数据
    dlg_main["生成估值余额对账数据"].check()
    sleep(1)
    #勾选发送估值余额对账数据
    dlg_main["发送估值余额对账数据"].check()
    sleep(1)

    #点击生成
    dlg_main["生 成"].set_focus()
    dlg_main["生 成"].click()
    sleep(1)
    status = True
    while status: #判断各种异常的弹框，都点确定
        #app.top_window().set_focus()
        try:
            if verify_control_exception(app.top_window(), []):
                send_email_to_admin("helloworld", "179770346@qq.com", "120315155@qq.com")
                sleep(300)

            fuck = app.top_window()["确定"]
            if app["基金资产估值表Dialog"]["产生完毕!"].exists():
                app["基金资产估值表Dialog"].set_focus()
                app["基金资产估值表Dialog"]["确定"].click()
                status = False
            else:
                fuck.click()
                sleep(1)
        except Exception:
            None

    #退出
    try:
        dlg_main.close()
    except timings.TimeoutError:
        app.top_window()["是(Y)"].set_focus()
        app.top_window()["是(Y)"].click()

if __name__ == "__main__":
    Shengcheng_guzhibiao("2018", "12", "13")