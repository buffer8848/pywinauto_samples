#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/09
# desc: 定义一些公共函数

#--------------------------------------------------------------------------------------------------

def restart_if_app_exist(exepath):
    from pywinauto.application import Application
    try:
        app = Application(backend="win32").connect(path=exepath)
        if app.is_process_running():
                app.kill()
    except Exception:
        None
		
#根据基金列表进行排序后，计算出其相对于屏幕的位置，用于鼠标点击选择操作
def choose_jijin_in_list(srclist, selectlist, jijinCurrent):
    from pywinauto.keyboard import SendKeys
    from time import sleep
    try:
        #srclist.sort()
        dict = {}
        number = 1
        current_number = 1
        for index in srclist:
            if(jijinCurrent == index):
                current_number = number
            dict[index] = number
            number += 1

        #匹配要选择的列表
        selectdict = {}
        for index in selectlist:
            if dict.get(str(index)) is not None:
                selectdict[index] = dict[index] - current_number
        #选择
        current = 0
        for (k, v) in selectdict.items():
            last_pose = v
            v -= current
            current = last_pose
            while v != 0:
                if v > 0:
                    SendKeys("{DOWN}")
                    v -= 1
                else:
                    SendKeys("{UP}")
                    v += 1
                sleep(0.5)
            SendKeys("{SPACE}")
            sleep(1)
    except Exception:
        None

#判断当前窗口句柄是否含有白名单字段
def verify_control_exception(control, whitelist):

    for index in whitelist:
        try:
            if (control[index].exist()):
                return True
        except Exception:
            None
    return False

#对当前窗口进行截图
def capture_current_screen():
    None

#发送邮件通知到指定的帐户
def send_email_to_admin(message, server, port, sender, pwd, reciever):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header("自动化测试程序", 'utf-8')   # 发送者
    message['To'] =  Header("自动化使用者", 'utf-8')        # 接收者
    
    subject = '自动化测试程序发生异常，请处理！'
    message['Subject'] = Header(subject, 'utf-8')
    
    smtpObj = smtplib.SMTP(server, port)
    smtpObj.login(sender, pwd)
    try:
        smtpObj.sendmail(sender, reciever, message.as_string())
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    smtpObj.quit()