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
import logging
# import openpyxl
import pysnooper
sys.path.append(os.path.abspath("../"))
import lib.ConfigSettings
BaseDir = lib.ConfigSettings.BaseDir
Cisco = lib.ConfigSettings.Cisco
CiscoGlobalCmd = lib.ConfigSettings.CiscoGlobalCmd
today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
DeviceName = ""
DeviceVendor = ""
GlobalErrorMessage = "Globally disable Dot1x"


def log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
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
        for d in dirs:
            DeviceVendor = d
        for f in files:
            DeviceName = f
            yield os.path.join(root, f)


# @pysnooper.snoop(prefix="generated_data: ")
def compare(files):
    data = []
    for file in files:
        data_dict = {DeviceName: {"Yes": {}, "No": {}}}
        if DeviceVendor == "Cisco":
            fd = '!'
            with open(file, 'r') as f:
                all_file = f.readlines()
            if CiscoGlobalCmd not in all_file:
                data_dict[DeviceName]["No"]["Message"] = GlobalErrorMessage
                logger.info("DeviceVendor:{0}, DeviceName:{1}, Message:{2}".format(DeviceVendor, DeviceName, GlobalErrorMessage))
                continue
        elif DeviceVendor == "H3C":
            pass
        else:
            logger.error("Unknown device vendor")
        f = iter(all_file)
        try:
            line = next(f)
            while line is not None and line != "":
                if "interface" in line and "Vlan" not in line:
                    txt_context = []
                    line_id = line.strip("\n ")
                    line = (next(f)).strip("\n ")
                    while fd not in line:
                        txt_context.append(line)
                        line = (next(f)).strip("\n ")
                    if DeviceVendor == "Cisco":
                        if not (set(Cisco) & set(txt_context) or set(Cisco) & set(txt_context)):
                            logger.info("DeviceVendor:{0}, DeviceName:{1}, InterfaceName:{2}".format(DeviceVendor, DeviceName, line_id))
                            data_dict[DeviceName]["No"][line_id] = txt_context
                    elif DeviceVendor == "H3C":
                        pass
                else:
                    line = next(f)
        except StopIteration:
            pass
        data.append(data_dict.copy())
    return data


# def data_to_excel(data):
#     table_title = ["DeviceName", "Interface", "Yes or No", "Detail"]
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     wb.save("..\\Result\\Result.xlsx")

def down_to_disk(r):
    with open("..\\result\\{0}.log".format(today), 'w') as f:
        f.write(json.dumps(r))


if __name__ == "__main__":
    logger = log()
    r = walk_file(BaseDir)
    r = compare(r)
    down_to_disk(r)

