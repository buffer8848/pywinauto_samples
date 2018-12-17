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

#根据基金列表进行排序后，计算出其相对于屏幕的位置，用于鼠标点击选择操作
def get_position_of_jijin_list(list, base=[103, 385], step = 15):
    try:
        #db = cx_Oracle.connect('SYSTEM/2wsxCDE#@yhsb/oral')
        #cursor = db.cursor()
        #result = cursor.execute("select ")
        list.sort()
        dict = {}
        x = base[0]
        y = base[1]
        for index in list:
            y += step
            dict[index] = [x, y]
        return dict
    except Exception:
        None


