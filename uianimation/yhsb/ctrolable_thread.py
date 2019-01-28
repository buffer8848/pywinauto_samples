#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2019/01/27
# desc: 可控的线程类

#--------------------------------------------------------------------------------------------------
import threading

class CrlableJob(threading.Thread):
    def __init__(self):
        ...
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.thing_done.set()
        self.can_run.set()

    def run(self):
        while True:
            self.can_run.wait()
            try:
                self.thing_done.clear()
                print
                'do the thing'
            finally:
                self.thing_done.set()

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.can_run.set()