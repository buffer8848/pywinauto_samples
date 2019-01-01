#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/08
# desc: 报表导出操作

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import mouse
from pywinauto import timings
from time import sleep

from common import *
from login import process_app_login

def Daochu_zichanbaobiao(year, month, day, blacklist, email_server_url, 
    email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected):
    exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssReport.exe"
    restart_if_app_exist(exepath)
    sleep(3)

    app = Application(backend="win32").start(exepath)

    #处理登录
    process_app_login(app)
    sleep(1)

    #---------------------------------------------------------------------------------------------------
    #打开报表左侧“资产估值表”
    dlg_main = app["ThunderRT6MDIForm"]
    dlg_main.set_focus()
    mouse.click(coords=(182,227)) #TODO
    sleep(1)
    mouse.click(coords=(78,347)) #TODO
    #dlg_main["ThunderRT6PictureBoxDC7"].set_focus()
    #dlg_main["ThunderRT6PictureBoxDC7"].click()
    sleep(1)

    #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    SendKeys("{ENTER}")
    sleep(2)

    #点击基金浏览
    dlg_main["基金列表>>"].set_focus()
    dlg_main["基金列表>>"].click()
    sleep(2)
    mouse.click(coords=(384,127))
    #mouse.click(coords=(406,145))
    #mouse.click(coords=(402,157))
    #点击浏 览
    dlg_main["浏 览"].set_focus()
    dlg_main["浏 览"].click()
    sleep(2)

    while True: #等待保存成功后的弹窗
        try:
            if verify_control_exception(app.top_window(), []):
                send_email_to_admin("helloworld", "179770346@qq.com", "120315155@qq.com")
                sleep(300)

            try:
                if not dlg_main["Progress Bar"].exist():
                    break
            except Exception:
                break
            app.top_window()["确定"].set_focus()
            app.top_window()["确定"].click()
            sleep(1)
        except Exception:
            None

    #点击保存excel
    dlg_main["msvb_lib_toolbar"].click(coords=(71,10))
    #输出excel
    dlg_outxls = app["输出EXCEL"]
    dlg_outxls.set_focus()
    dlg_outxls.Edit2.set_text(r"C:\tool\buffer\data")
    dlg_outxls.Edit3.set_text(r"对帐结果管理.xls")
    dlg_outxls["确 定"].click()
    sleep(2)

    #等待保存的进度条出现
    while True: #等待保存成功后的弹窗
        try:
            if verify_control_exception(app.top_window(), []):
                send_email_to_admin("helloworld", "179770346@qq.com", "120315155@qq.com")
                sleep(300)

            try:
                app["导出EXCEL文件Dialog"]["是(Y)"].set_focus()
                app["导出EXCEL文件Dialog"]["是(Y)"].click()
            except Exception:
                None
            try:
                if dlg_outxls["ProgressBar20WndClass"].exists():
                    break
            except Exception:
                None
        except Exception:
            None

    #等待进度条完成
    while True: #等待保存成功后的弹窗
        try:
            if verify_control_exception(app.top_window(), []):
                send_email_to_admin("helloworld", "179770346@qq.com", "120315155@qq.com")
                sleep(300)
                
            try:
                app["导出EXCEL文件Dialog"]["确定"].set_focus()
                app["导出EXCEL文件Dialog"]["确定"].click()
                sleep(1)
            except Exception:
                None
            try:
                if not dlg_outxls["ProgressBar20WndClass"].exists():
                    break
            except Exception:
                break
        except Exception:
            None

    #退出
    try:
        dlg_main.close()
    except timings.TimeoutError:
        app.top_window()["是(Y)"].click()