#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/2/5 12:10
"""

import sys
import os
import json
import datetime
# import openpyxl
sys.path.append(os.path.abspath("../"))
import lib.ConfigSettings

today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
BaseDir = lib.ConfigSettings.BaseDir
Cisco = lib.ConfigSettings.Cisco
CiscoGlobalCmd = lib.ConfigSettings.CiscoGlobalCmd
DeviceName = ""
DeviceVendor = ""


def log(level):
    import logging
    go_level = {"info": logging.INFO, "error": logging.ERROR, "debug": logging.DEBUG, "warning": logging.WARNING,
                "critical": logging.CRITICAL}
    logger = logging.getLogger()
    logger.setLevel(go_level[level])
    fh = logging.FileHandler('..\\log\\{0}.log'.format(today))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def walk_file(base):
    global DeviceName, DeviceVendor
    for root, dirs, files in os.walk(base):
        for f in files:
            DeviceName = f
            DeviceVendor = root.strip("..\\data\\")
            yield os.path.join(root, f)


# @pysnooper.snoop(prefix="generated_data: ")
def combing(files):
    for file in files:
        data_dict = {}
        with open(file) as f:
            file_context = f.readlines()
            f = iter(file_context)
            try:
                line = next(f)
                while line is not None and line != "":
                    if "interface" in line and "Vlan" not in line:
                        if_id = line
                        line = next(f)
                        while True:
                            if " description" in line:
                                data_dict[if_id] = line
                            break
                    else:
                        line = next(f)
            except StopIteration:
                pass
        logger.debug("DeviceVendor: {0}, DeviceName: {1}".format(DeviceVendor, DeviceName))
        logger.debug(data_dict)
        write_to_excel(data_dict)
    workbook.close()


def data_to_excel():
    import xlsxwriter
    workbook = xlsxwriter.Workbook('..\\Result\\Result.xlsx')
    return workbook


def write_to_excel(d):
    worksheet = workbook.add_worksheet(DeviceName)
    row = 0
    col = 0
    for key in d.keys():
        worksheet.write(row, col, key)
        worksheet.write(row, col+1, d[key])
        row += 1


if __name__ == "__main__":
    logger = log("debug")
    r = walk_file(BaseDir)
    workbook = data_to_excel()
    combing(r)
