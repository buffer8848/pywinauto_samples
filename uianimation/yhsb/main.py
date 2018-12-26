#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/09
# desc: 报所有的流程串起来

#-------------------------------------------------------------------------------------------------
from time import sleep

from data_import import Daochu_shuju
from make_pingzheng import Zhizuo_pingzheng
from dianziduizhangguanli import Guanli_dianziduizhang
from shengchengguzhibiao import Shengcheng_guzhibiao
from zichan_baobiaodaochu import Daochu_zichanbaobiao
from toucun_baobiaodaochu import Daochu_toucunbaobiao

if __name__ == "__main__":
    year = "2018"
    month = "12"
    number = 0
    run_count = 0;
    while True:
        number += 1
        if number > 31:
            number = 1
        day = "%02d" % (number)
        Daochu_shuju(year, month, day)
        sleep(5)
        Zhizuo_pingzheng(year, month, day)
        sleep(5)
        Guanli_dianziduizhang(year, month, day)
        sleep(5)
        Shengcheng_guzhibiao(year, month, day)
        sleep(5)
        Daochu_zichanbaobiao(year, month, day)
        sleep(5)
        Daochu_toucunbaobiao(year, month, day)
        sleep(5)

        run_count += 1
        print("auto runing count:" + str(run_count))
