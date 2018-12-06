#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/04
# desc: 生成估值表
#--------------------------------------------------------------------------------------------------

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import timings
from time import sleep

app = Application().start(r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe")

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
send_keys("2018")
send_keys("{RIGHT}")
send_keys("12")
send_keys("{RIGHT}")
send_keys("05")

#勾选生成估值余额对账数据
dlg_main["生成估值余额对账数据"].check()
sleep(1)
#勾选发送估值余额对账数据
dlg_main["发送估值余额对账数据"].check()
sleep(1)

#点击生成
ctl_gen = dlg_main["生 成"]
ctl_gen.click()
sleep(1)
status = True
while status: #判断各种异常的弹框，都点确定
    try:
        if app["基金资产估值表Dialog"]["产生完毕!"].exists():
            app["基金资产估值表Dialog"].set_focus()
            app["基金资产估值表Dialog"]["确定"].click()
            status = False
        app.top_window()["确定"].set_focus()
        app.top_window()["确定"].click()
        sleep(1)
    except Exception:
        None

#退出

try:
    dlg_main.close()
except timings.TimeoutError:
    app.top_window()["是(Y)"].set_focus()
    app.top_window()["是(Y)"].click()
