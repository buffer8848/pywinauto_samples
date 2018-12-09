#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/09
# desc: 定义一些公共函数

#--------------------------------------------------------------------------------------------------
from pywinauto.application import Application

def restart_if_app_exist(exepath):
    try:
        app = Application(backend="win32").connect(path=exepath)
        if app.is_process_running():
                app.kill()
    except Exception:
        None