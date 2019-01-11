#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------


def Daochu_shuju(exePath, filePath, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW,
                 year, month, day, blacklist, email_server_url, email_server_port, sender_email, sender_passwd,
                 reciever_email, jijinListTotal, jijinListSelected):
    from pywinauto.application import Application
    from pywinauto.keyboard import send_keys
    from pywinauto import mouse
    from pywinauto import timings
    from time import sleep
    from common import restart_if_app_exist, verify_control_exception, send_email_to_admin, get_position_of_jijin_list
    from login import process_app_login

    # exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    restart_if_app_exist(gzPath)
    sleep(3)
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
    send_keys(year)
    send_keys("{RIGHT}")
    send_keys(month)
    send_keys("{RIGHT}")
    send_keys(day)
    send_keys("{ENTER}")
    sleep(2)

    #输入文件路径
    dlg_main["按时间段读取Edit2"].set_text(filePath)

    #进入到数据管理页面
    ctl_treedview = dlg_main["TreeView20WndClass"]
    ctl_treedview.set_focus()
    # SendKeys("{LEFT}")
    # gd.getCtn1()

    # 选择基金
    current = 0;
    dict = get_position_of_jijin_list(jijinListTotal, jijinListSelected, [100, 305], 15)
    for (k, v) in dict.items():
        dlg_main["TreeView20WndClass1"].set_focus()
        while current < v:
            SendKeys("{DOWN}")
            current += 1
        SendKeys("{SPACE}")
        #mouse.click(coords=(v[0]-40, v[1]))
        #mouse.click(coords=(v[0], v[1]))
    sleep(1)
    ctl_treedview = dlg_main["TreeView20WndClass2"]
    ctl_treedview.set_focus()
    ctl_treedview.click(coords=(60, 100))
    sleep(1)
    dlg_main["读取数据"].set_focus()
    dlg_main["读取数据"].click()
    sleep(1)
    while True: #等待保存成功后的弹窗
        try:
            if verify_control_exception(app.top_window(), blacklist):
                send_email_to_admin("helloworld", email_server_url, email_server_port, sender_email, sender_passwd, reciever_email)
                sleep(300)
            try:
                if app["数据接口管理Dialog"]["读取完毕"].exists():
                    app["数据接口管理Dialog"].set_focus()
                    app["数据接口管理Dialog"]["确定"].click()
                    break
            except Exception:
                None
            SendKeys("{ENTER}")
            #app.top_window()["是(Y)"].set_focus()
            #app.top_window()["是(Y)"].click()
            sleep(1)
        except Exception:
            None

    #退出
    try:
        dlg_main.close()
    except timings.TimeoutError:
        app.top_window()["是(Y)"].click()