#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/01
# desc: 实现打开一个notepad，写入一个helloworld，然后保存到指定的位置

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application
# Run a target application
app = Application().start("notepad.exe")

app.Notepad.Edit.set_text("hello world.");

app.Notepad.menu_select("文件(F)->保存(S)")

dialog = app["另存为"]
dialog.Edit.set_text("hello.txt");
dialog.SaveButton.click();

