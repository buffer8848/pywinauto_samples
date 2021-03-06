#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------


def Daochu_shuju(exePath, imPath, exPath, jijinCurrent, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW,
                 year, month, day, blacklist, email_server_url, email_server_port, sender_email, sender_passwd,
                 reciever_email, jijinListTotal, jijinListSelected, single, cntnDo):
    from pywinauto.application import Application
    from pywinauto.keyboard import SendKeys
    from pywinauto import mouse
    from pywinauto import timings
    from time import sleep
    from common import restart_if_app_exist, verify_control_exception, send_email_to_admin, choose_jijin_in_list
    from login import process_app_login

    # exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    # restart_if_app_exist(gzPath)
    # sleep(3)
    app = Application(backend="win32").start(gzPath)

    process_app_login(app, gzName, gzPW)
    sleep(3)


    #打开数据管理
    dlg_main = app["ThunderRT6MDIForm"]
    dlg_main.set_focus()
    ctl_sysnvg = dlg_main["系统功能导航"]
    ctl_sysnvg.ThunderRT6UserControlDC6.click()
    sleep(3)

    # #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    SendKeys("{ENTER}")
    sleep(2)

    #输入文件路径
    dlg_main["按时间段读取Edit2"].set_text(imPath)

    #进入到数据管理页面
    ctl_treedview = dlg_main["TreeView20WndClass"]
    ctl_treedview.set_focus()
    # SendKeys("{LEFT}")
    # gd.getCtn1()

    # 选择基金
    dlg_main["TreeView20WndClass1"].set_focus()
    choose_jijin_in_list(jijinListTotal, jijinListSelected, jijinCurrent)
    sleep(1)
    ctl_treedview = dlg_main["TreeView20WndClass2"]
    ctl_treedview.set_focus()
    ctl_treedview.click(coords=(60, 100))
    sleep(1)
    dlg_main["读取数据"].set_focus()
    dlg_main["读取数据"].click()
    sleep(1)
    status = True
    while status: #等待保存成功后的弹窗
        sleep(1)
        print(status)
        try:
            if verify_control_exception(app.top_window(), blacklist):
                send_email_to_admin("helloworld", email_server_url, email_server_port, sender_email, sender_passwd,
                                    reciever_email, None, 0)
                stt = True
                while stt:
                    sleep(20)
                    if verify_control_exception(app.top_window(), blacklist):
                        continue
                    else:
                        stt = False
            try:
                if app["数据接口管理Dialog"]["读取完成"].exists():
                    print(3)
                    status = False
            except Exception:
                None
            try:
                app.top_window()["确定"].set_focus()
                app.top_window()["确定"].click()
            except Exception:
                None
            try:
                app.top_window()["是(Y)"].set_focus()
                app.top_window()["是(Y)"].click()
            except Exception:
                None
        except Exception:
            None

    # #退出
    if single == 1:
        try:
            dlg_main.close()
        except timings.TimeoutError:
            app.top_window()["是(Y)"].click()
    elif cntnDo == 1:
        dlg_main["退    出"].click()