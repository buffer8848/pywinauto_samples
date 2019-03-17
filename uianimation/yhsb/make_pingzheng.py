#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 针对某基金软件进行模拟操作

#--------------------------------------------------------------------------------------------------

def Zhizuo_pingzheng(exePath, imPath, exPath, jijinCurrent, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW,
                     year, month, day, blacklist, email_server_url, email_server_port, sender_email,
                     sender_passwd, reciever_email, jijinListTotal, jijinListSelected, single, cntnDo):
    from pywinauto.application import Application
    from pywinauto.keyboard import SendKeys
    from pywinauto import timings
    from time import sleep
    from common import restart_if_app_exist, verify_control_exception, send_email_to_admin, choose_jijin_in_list
    from login import process_app_login
    # if (True): #外部加个参数控制是否需要重新登陆
    #     restart_if_app_exist(gzPath)
    #     sleep(3)
    #     app = Application().start(gzPath)
    #     #处理登录
    #     process_app_login(app, gzName, gzPW)
    # else:
    #     app = Application(backend="win32").connect(path=gzPath)
    # sleep(3)
    if single == 1:
        restart_if_app_exist(gzPath)
        sleep(3)
        app = Application().start(gzPath)
        #处理登录
        process_app_login(app, gzName, gzPW)
    else:
        app = Application(backend="win32").connect(path=gzPath)
        print(app)

    #打开数据管理
    dlg_main = app["ThunderRT6MDIForm"]
    ctl_sysnvg = dlg_main["系统功能导航"]
    ctl_sysnvg.ThunderRT6UserControlDC5.click()
    sleep(3)

    #输入日期
    dlg_main["DTPicker20WndClass3"].set_focus()
    SendKeys(year)
    SendKeys("{RIGHT}")
    SendKeys(month)
    SendKeys("{RIGHT}")
    SendKeys(day)
    sleep(2)

    # 选择基金
    dlg_main["TreeView20WndClass2"].set_focus()
    choose_jijin_in_list(jijinListTotal, jijinListSelected, jijinCurrent)

    #进入到数据管理页面
    ctl_treedview = dlg_main["非结转损益"]
    ctl_treedview.check()
    sleep(1)
    dlg_main["制作凭证"].set_focus()
    dlg_main["制作凭证"].click()
    sleep(1)
    status = True
    num = 0
    while status: #判断各种异常的弹框，都点yes
        print(status)
        try:
            if verify_control_exception(app.top_window(), blacklist):
                send_email_to_admin("helloworld", email_server_url, email_server_port, sender_email, sender_passwd,
                                    reciever_email, None, 0)
                stt = True
                while stt:
                    sleep(60)
                    if verify_control_exception(app.top_window(), blacklist):
                        continue
                    else:
                        stt = False

            try:
                if app["业务凭证管理Dialog"]["凭证制作完毕!"].exists():
                    print(3)
                    app.top_window()["确定"].set_focus()
                    app.top_window()["确定"].click()
                    status = False
                else:
                    app.top_window()["确定"].set_focus()
                    app.top_window()["确定"].click()
            except Exception:
                None
            #SendKeys("{ENTER}")
            try:
                app.top_window()["是(Y)"].set_focus()
                app.top_window()["是(Y)"].click()
            except Exception:
                None
        except Exception:
            None

    #退出
    if single == 1:
        try:
            dlg_main.close()
        except timings.TimeoutError:
            app.top_window()["是(Y)"].click()
    elif cntnDo == 1:
        dlg_main["退    出"].click()

    #dlg_login.print_control_identifiers()