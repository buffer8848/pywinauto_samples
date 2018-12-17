#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# auth: libinfei/179770346@qq.com
# time: 2018/12/09
# desc: 处理excel表

#--------------------------------------------------------------------------------------------------
import xlrd
import openpyxl

def Merge_excels(heduijingzhi_excel, toucun_excel, zichan_excel, outputexcel):
    #先打开核对净值总表
    hedui_data = openpyxl.load_workbook(heduijingzhi_excel)

    #得到头寸excel表
    hedui_toucun_sheet = hedui_data["估值-头寸预测表"] #追加的方式
    toucun_data = xlrd.open_workbook(toucun_excel) 
    toucun_sheet = toucun_data.sheet_by_index(0)
    for row in range(1, toucun_sheet.nrows):
        for col in range(1, toucun_sheet.ncols):
            hedui_toucun_sheet.cell(row, col, toucun_sheet.cell(row, col).value)

    #合并估值-资产情况表
    hedui_zichan_sheet = hedui_data["估值-资产情况表"] #追加的方式
    zichan_data = xlrd.open_workbook(zichan_excel) 
    zichan_sheet = zichan_data.sheet_by_index(0)
    for row in range(1, zichan_sheet.nrows):
        for col in range(1, zichan_sheet.ncols):
            hedui_zichan_sheet.cell(row, col, zichan_sheet.cell(row, col).value)

    #保存
    hedui_data.save(outputexcel)


if __name__ == "__main__":
    heduijingzhi_excel = r"D:\work\uiauto\yhsb\uianimation\核对净值示范空表.xlsx"
    toucun_excel = r"D:\work\uiauto\yhsb\uianimation\180003银华-道琼斯88指数资产情况统计表.xls"
    zichan_excel = r"D:\work\uiauto\yhsb\uianimation\1800032018年12月05日银华-道琼斯88指数现金头寸预测汇总表.xls"
    outputexcel = r"D:\work\uiauto\yhsb\uianimation\核对净值表.xlsx"
    Merge_excels(heduijingzhi_excel, toucun_excel, zichan_excel, outputexcel)