#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/09
# desc: 基金资产表导出

#--------------------------------------------------------------------------------------------------

def Daochu_jijinzichan(exePath, imPath, exPath, fundName, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW, year, month, day, blacklist, email_server_url, email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal, jijinListSelected):
    from pywinauto.application import Application
    from pywinauto.keyboard import SendKeys
    from pywinauto import timings
    from time import sleep
    from pywinauto import mouse
    from common import restart_if_app_exist, verify_control_exception, send_email_to_admin
    from login import process_app_login
    # exepath = r"F:\O32测试环境\trade\trade.exe"
    restart_if_app_exist(o32Path)
    sleep(3)
    app = Application(backend="win32").start(o32Path)

    #如果有提示更新，点击确定
    sleep(1)
    SendKeys("{ENTER}")
    sleep(1)
    try:
        app["提示"]["确定"].set_focus()
        app["提示"]["确定"].click()
        sleep(2)
    except Exception:
        None

    #登陆
    app["TfrmLogin"].wait('exists enabled visible ready')
    app["TfrmLogin"].set_focus()
    app["TfrmLogin"]["登录Edit2"].set_text("0")
    sleep(2)
    app["TfrmLogin"]["登录Button"].set_focus()
    app["TfrmLogin"]["登录Button"].click()
    sleep(5)

    #如果有警告，点击是
    try:
        app["警告"]["是(Y)"].set_focus()
        app["警告"]["是(Y)"].click()
        sleep(5)
    except Exception:
        None

    try:
        app["自动更新"].set_focus() # 自动更新界面点关闭
        app["自动更新"]["关闭(Esc/Enter)"].click()
        sleep(5)
        app["警告"]["是(Y)"].set_focus()
        app["警告"]["是(Y)"].click()
        sleep(5)
    except Exception:
        None

    #主界面出现
    dlg_main = app["TfrmMain"]
    dlg_main.wait('exists enabled visible ready')

    #先选择菜单，再模拟点击
    dlg_main.Static.TOutlookBar.TOutlookSection0.TreeView.wrapper_object().select("\\n综合信息查询")
    sleep(1)
    SendKeys("{ENTER}")
    #点击信息查询->综合信息查询
    #mouse.click(coords=(86,780)) #TODO
    #sleep(3)
    #mouse.click(coords=(68,311)) #TODO
    sleep(5)

    #等待综合信息查询界面出现
    #dlg_main["基金资产[4]"].wait('exists enabled visible ready')
    #dlg_main["基金资产[4]"].set_focus()
    #dlg_main["基金资产[4]"].click()

    sleep(1)
    mouse.click(coords=(324,118)) #TODO
    sleep(3)
    mouse.click(coords=(137,89)) #TODO
    SendKeys("-1")
    sleep(2)
    mouse.click(coords=(142,109)) #TODO
    #dlg_main["THsEdit"].set_text("-1  所有基金")
    #dlg_main["THsEdit"].set_text("2  银华优势")
    sleep(20)

    #点击输出框后点保存
    dlg_main["TPanel"].set_focus()
    mouse.click(coords=(455,142)) #TODO
    sleep(5)
    app["另存为"]["保存(S)"].set_focus()
    app["另存为"]["保存(S)"].click()
    sleep(1)
    SendKeys("{LEFT}")
    sleep(1)
    SendKeys("{ENTER}")
    sleep(3)

    #qiut
    try:
        dlg_main.close()
    except timings.TimeoutError:
        app.top_window()["是(Y)"].click()

    #dlg_main["信息查询TOutlookSection"].set_focus()
    #dlg_main["信息查询TOutlookSection"].click()


if __name__ == "__main__":
    Daochu_jijinzichan()