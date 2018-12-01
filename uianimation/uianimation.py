#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/01
# desc: 实现打开一个notepad，写入一个helloworld，然后保存到指定的位置

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
from pywinauto import timings

# Run a target application
app = Application().start("notepad.exe")

app.Notepad.Edit.set_text("hello world.")

app.Notepad.menu_select("文件(F)->保存(S)")

dlg_save = app["另存为"]
dlg_save.Edit.set_text("hello.txt")
dlg_save["保存(&S)"].click()

#如果有此文件，弹出覆盖框，点击确定覆盖
dlg_save_replace = app["确认另存为"]
try:
    dlg_save_replace.wait("exists enabled visible ready", timeout=1)
    dlg_save_replace["是(&Y)"].click()
except TimeoutError:
    None

app.Notepad.close()

