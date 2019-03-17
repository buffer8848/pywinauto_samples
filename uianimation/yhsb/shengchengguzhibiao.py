#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/04
# desc: 生成估值表
#--------------------------------------------------------------------------------------------------


def Shengcheng_guzhibiao(exePath, imPath, exPath, jijinCurrent, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW,
                         year, month, day, blacklist, email_server_url, email_server_port, sender_email,
                         sender_passwd, reciever_email, jijinListTotal, jijinListSelected, single, cntnDo):
    from pywinauto.application import Application
    from pywinauto.keyboard import SendKeys
    from pywinauto import timings
    from time import sleep
    from pywinauto import mouse
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
    #
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
    dlg_main.set_focus()
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

    # 选择基金
    dlg_main["TreeView20WndClass2"].set_focus()
    choose_jijin_in_list(jijinListTotal, jijinListSelected, jijinCurrent)

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

            fuck = app.top_window()["确定"]
            if app["基金资产估值表Dialog"]["产生完毕!"].exists():
                app["基金资产估值表Dialog"].set_focus()
                app["基金资产估值表Dialog"]["确定"].click()
                status = False
            else:
                #SendKeys("{ENTER}")
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
