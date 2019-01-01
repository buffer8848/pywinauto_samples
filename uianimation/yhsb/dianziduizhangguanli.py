#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/05
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import timings
from time import sleep

from common import *
from login import process_app_login

def Guanli_dianziduizhang(year, month, day, blacklist, email_server_url, 
    email_server_port, sender_email, sender_passwd, reciever_email, jijinListTotal, jijinListSelected):
    exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    restart_if_app_exist(exepath)
    sleep(3)

    app = Application(backend="win32").start(exepath)

    #处理登录
    process_app_login(app)
    sleep(1)

    #打开数据管理
    dlg_main = app["ThunderRT6MDIForm"]
    dlg_main.set_focus()
    ctl_sysnvg = dlg_main["系统功能导航"]
    ctl_sysnvg.ThunderRT6UserControlDC6.click()
    sleep(1)

    #点击电子对账管理
    dlg_main.set_focus()
    dlg_main.menu_select("电子对帐 -> 对帐结果管理")
    sleep(1)
    dlg_main["查询"].set_focus()
    dlg_main["查询"].click()

    #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    sleep(2)

    #点击右键菜单
    dlg_main["数据管理"].set_focus()
    dlg_main["数据管理"].ThunderRT6UserControlDC.click(button=u'right', coords=(300,300))
    #选择菜单
    #app.menu_select["报表输出 -> 输出为Excel文件"]
    SendKeys("{DOWN 6}")
    sleep(2)
    SendKeys("{RIGHT}")
    sleep(2)
    SendKeys("{ENTER}")

    #输出excel
    dlg_outxls = app["输出EXCEL"]
    dlg_outxls.set_focus()
    dlg_outxls.Edit2.set_text(r"F:\tool\buffer\data")
    dlg_outxls.Edit3.set_text(r"对帐结果管理.xls")
    sleep(2)
    dlg_outxls["确 定"].set_focus()
    dlg_outxls["确 定"].click()
    sleep(3)

    while True: #等待保存成功后的弹窗
        try:
            if verify_control_exception(app.top_window(), []):
                send_email_to_admin("helloworld", "179770346@qq.com", "120315155@qq.com")
                sleep(300)
                
            try:
                if app["导出EXCEL文件Dialog"]["确定"].exists():
                    app["导出EXCEL文件Dialog"].set_focus()
                    app["导出EXCEL文件Dialog"]["确定"].click()
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