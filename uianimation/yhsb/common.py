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
#startflag = True表示从头开始，负责从当前选中位置开始
#currentflag = True表示选择当前，False表示不选当前
def choose_jijin_in_list(srclist, selectlist, jijinCurrent, currentflag=False, startflag = False):
    from pywinauto.keyboard import SendKeys
    from time import sleep
    try:
        dict = {}
        list = []
        number = 1
        current_number = 0
        for index in srclist:
            if jijinCurrent == index:
                current_number = number
            dict[index] = number
            number += 1
        if startflag is True:
            current_number = 1
        if currentflag is False:
            list.append(dict[jijinCurrent] - current_number)
        #匹配要选择的列表
        for index in selectlist:
            if dict.get(str(index)) is not None:
                list.append(dict[index] - current_number)
        current = 0
        for v in list:
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
                sleep(1)
            SendKeys("{SPACE}")
            sleep(0.5)
            SendKeys("{ESC}")
            sleep(1)
    except Exception:
        None

#判断当前窗口句柄是否含有白名单字段
def verify_control_exception(control, whitelist):
    for index in whitelist:
        try:
            control.set_focus()
            print(control.wrapper_object().texts())
            if control.wrapper_object().texts().__str__().find(index) > 0:
                return True
            if control._ctrl_identifiers().values().__str__().find(index) > 0:
                return True
        except Exception:
            None
    return False

#对当前窗口进行截图
def capture_current_screen():
    from PIL import ImageGrab
    imagepath = "tmp.jpg"
    im = ImageGrab.grab()
    im.save(imagepath, 'jpeg')
    return imagepath

#发送邮件通知到指定的帐户
def send_email_to_admin(text, server, port, sender, pwd, reciever, attachfile, flag, times=0):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    from email.mime.base import MIMEBase
    from email import encoders
    import os

    try:
        smtpObj = smtplib.SMTP(server, port)
        smtpObj.login(sender, pwd)

        if flag == 1:
            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
            message = MIMEMultipart()
            message['From'] = Header("自动化测试程序", 'utf-8')  # 发送者
            message['To'] = Header("自动化使用者", 'utf-8')  # 接收者

            subject = '第'+ str(times) +'次对账结果'
            message['Subject'] = Header(subject, 'utf-8')
            message.attach(MIMEText(text))
        elif flag == 0:
            message = MIMEMultipart()
            message['From'] = Header("自动化测试程序", 'utf-8')  # 发送者
            message['To'] = Header("自动化使用者", 'utf-8')  # 接收者

            subject = '自动化测试程序发生异常，请处理！'
            message['Subject'] = Header(subject, 'utf-8')
            message.attach(MIMEText(text))
        elif flag == 2:
            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
            message = MIMEMultipart()
            message['From'] = Header("自动化测试程序", 'utf-8')  # 发送者
            message['To'] = Header("自动化使用者", 'utf-8')  # 接收者

            subject = '净值核对结果'
            message['Subject'] = Header(subject, 'utf-8')
            message.attach(MIMEText(text))

        # 带上二进制附件
        if attachfile is None:
            attachfile = capture_current_screen()
        if attachfile is not None:
            part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
            part.set_payload(open(attachfile, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachfile))
            message.attach(part)

        smtpObj.sendmail(sender, reciever, message.as_string())
    except Exception:
        print("Error: 无法发送邮件")
    smtpObj.quit()
