#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/04
# desc: 生成估值表
#--------------------------------------------------------------------------------------------------


def Shengcheng_guzhibiao(exePath, imPath, exPath, jijinCurrent, gzPath, gzName, gzPW, cwPath, cwName, cwPW, o32Path, o32Name, o32PW,
                         year, month, day, blacklist, email_server_url, email_server_port, sender_email,
                         sender_passwd, reciever_email, jijinListTotal, jijinListSelected):
    from pywinauto.application import Application
    from pywinauto.keyboard import send_keys, SendKeys
    from pywinauto import timings
    from time import sleep
    from pywinauto import mouse
    from common import restart_if_app_exist, verify_control_exception, send_email_to_admin, choose_jijin_in_list
    from login import process_app_login

    # exepath = r"C:\Program Files (x86)\赢时胜资产财务估值系统V2.5\YssGz.exe"
    restart_if_app_exist(gzPath)
    sleep(3)

    app = Application().start(gzPath)

    #处理登录
    process_app_login(app, gzName, gzPW)
    sleep(1)

    #打开数据管理
    dlg_main = app["ThunderRT6MDIForm"]
    ctl_sysnvg = dlg_main["msvb_lib_toolbar"]
    ctl_sysnvg.click(coords=(415,15))
    sleep(1)

    #输入日期
    dlg_main["DTPicker20WndClass2"].set_focus()
    send_keys(year)
    send_keys("{RIGHT}")
    send_keys(month)
    send_keys("{RIGHT}")
    send_keys(day)
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
                                    reciever_email, exPath + "/对帐结果管理.xls")
                sleep(300)

            fuck = app.top_window()["确定"]
            if app["基金资产估值表Dialog"]["产生完毕!"].exists():
                app["基金资产估值表Dialog"].set_focus()
                app["基金资产估值表Dialog"]["确定"].click()
                status = False
            else:
                send_keys("{ENTER}")
                #fuck.click()
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
