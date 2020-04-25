# -*- coding: UTF-8 -*-
# @Time    : 2020/1/3 13:09
# @Author  : LiuYuBo
# @Software: PyCharmCM

import sys
import os
import openpyxl
import datetime
import paramiko
import json

sys.path.append(os.path.abspath("../"))
import lib.BackupConfigSettings
XLSX_Path = lib.BackupConfigSettings.XLSX_Path
DataDict = lib.BackupConfigSettings.DataDict
Global_ErrorMess = lib.BackupConfigSettings.Global_ErrorMess
FtpServerIP = lib.BackupConfigSettings.FtpServerIP
FtpServerUsername = lib.BackupConfigSettings.FtpServerUsername
FtpServerPassword = lib.BackupConfigSettings.FtpServerPassword
FtpServerRoot = lib.BackupConfigSettings.FtpServerRoot
H3C = lib.BackupConfigSettings.H3C
MaiPu = lib.BackupConfigSettings.MaiPu
Cisco = lib.BackupConfigSettings.Cisco
run_cmd_dict = lib.BackupConfigSettings.run_cmd_dict
H3C_Cv7 = lib.BackupConfigSettings.H3C_Cv7

today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


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


def common_ssh(ssh):
    try:
        ssh.connect(hostname=DataDict['地址'], port=22, username=DataDict['用户名'], password=DataDict['密码'],
                    look_for_keys=False, timeout=3)
    except Exception as r:
        logger.error("设备名称: {0} 设备地址: {1} 错误: {2}".format(DataDict['设备名称'], DataDict['地址'], r))
    else:
        if DataDict['设备厂商'] == "H3C-v7":
            stdin, stdout, stderr = ssh.exec_command(
                H3C_Cv7.format(FtpServerUsername, FtpServerPassword, FtpServerIP, DataDict['设备名称'], today))
            b_result = stdout.read()
            r = bytes.decode(b_result)
            logger.debug(r)
        else:
            channel = ssh.invoke_shell(height=999)
            stdin = channel.makefile('wb')
            stdout = channel.makefile('rb')
            run_cmd = DataDict['设备厂商']
            stdin.write(
                run_cmd_dict[run_cmd].format(FtpServerIP, FtpServerUsername, FtpServerPassword, DataDict['设备名称'], today,
                                             DataDict['地址'], DataDict['Enable密码']))
            r = stdout.read().decode('gbk')
            logger.debug(r)
    finally:
        ssh.close()


def make_dir(wb_sheet, max_column, max_row):
    all_device_vendor = []
    for i in range(1, max_column + 1):
        DataDict.setdefault(wb_sheet.cell(1, i).value)
        if wb_sheet.cell(1, i).value == "设备厂商":
            DeviceVendor_ColNum = i
    for i in range(2, max_row + 1):
        all_device_vendor.append(wb_sheet.cell(i, DeviceVendor_ColNum).value)
    all_device_vendor = set(all_device_vendor)
    all_device_vendor.discard("H3C-v7")
    for i in all_device_vendor:
        os.makedirs(("{}\\{}\\{}".format(FtpServerRoot, today, i)))


def core(max_row, max_column, wb_sheet, ssh):
    for i in range(1, max_column + 1):
        DataDict.setdefault(wb_sheet.cell(1, i).value)
    for i in range(2, max_row + 1):
        for j in range(1, max_column + 1):
            DataDict[wb_sheet.cell(1, j).value] = wb_sheet.cell(i, j).value
        common_ssh(ssh)


def main(sheet_name):
    global Global_ErrorMess
    wb = openpyxl.load_workbook(XLSX_Path)
    wb_sheet = wb[sheet_name]
    max_column = wb_sheet.max_column
    max_row = wb_sheet.max_row
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    make_dir(wb_sheet, max_column, max_row)
    core(max_row, max_column, wb_sheet, ssh)
    wb.close()


if __name__ == "__main__":
    logger = log("info")
    main("WorkNet")