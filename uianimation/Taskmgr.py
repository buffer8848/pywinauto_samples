#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 找到进程，将其kill

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application

app = Application().connect(title="任务管理器")
app.TaskManagerWindow.set_focus()
dlg_main = app.TaskManagerWindow["SysListView32"]
for item in dlg_main.items():
    print(item.item_data())
    item.select()
    if item.text() == "wpscenter.exe":
        print(item.Text())