#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/02
# desc: 找到进程，将其kill

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application

app = Application(backend='uia').connect(title="任务管理器")
app.Dialog.set_focus()
dlg_main = app.Dialog.Pane.ListBox
item = dlg_main.ListItem
for item in dlg_main.items():
    #print(item.item_data())
    #item.select()
    try:
        if item.text() == "wpscenter.exe":
                print(item.Text())
    except Exception:
            pass
