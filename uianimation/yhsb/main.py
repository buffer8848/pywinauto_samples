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
    blacklist = ['异常', 'error'] #存放用户遇到这些窗口之后就停止的黑名单
    email_server_url = "smtp.qq.com" #发送邮件的服务器地址
    email_server_port = 25 #发送邮件的服务器端口
    sender_email = '179770346@qq.com' #发送邮件的账号
    reciever_email = '120315155@qq.com' #接收邮件的账号

    jijinListTotal = ["A003_银华保本增值混合", "A004_银华-道琼斯88指数", "A005_银华货币", "A006_银华价值优选股票", "A002_银华优势企业混合"] #存放基金总表
    jijinListSelected = ["A003_银华保本增值混合", "A002_银华优势企业混合"] #存放要选择的基金

    run_count = 0
    while True:
        number += 1
        if number > 31:
            number = 1
        day = "%02d" % (number)
        Daochu_shuju(year, month, day, blacklist, email_server_url,
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)
        Zhizuo_pingzheng(year, month, day, blacklist, email_server_url, 
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)
        Guanli_dianziduizhang(year, month, day, blacklist, email_server_url, 
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)
        Shengcheng_guzhibiao(year, month, day, blacklist, email_server_url, 
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)
        Daochu_zichanbaobiao(year, month, day, blacklist, email_server_url, 
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)
        Daochu_toucunbaobiao(year, month, day, blacklist, email_server_url, 
            email_server_port, sender_email, reciever_email, jijinListTotal, jijinListSelected)
        sleep(5)

        run_count += 1
        print("auto runing count:" + str(run_count))
