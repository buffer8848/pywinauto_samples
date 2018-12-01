#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 找到qq，然后找到联系人发送信息
#       TODO(qq是dui的目前无法找到好的办法遍历里面的控件，暂时搁置)

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application

app = Application().connect(path=r"C:\Program Files (x86)\Tencent\QQ\Bin\qq.exe").TXGuiFoundation
app.set_focus()
app['莫恒等5个会话'].print_control_identifiers()