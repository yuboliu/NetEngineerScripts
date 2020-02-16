#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/1/20 10:58
"""

import sys
import os
# import openpyxl
import json
# import urllib3
import requests
import pysnooper
from InternalUser import generated_data
from InternalUser import before_end
from InternalUser import echo_result

sys.path.append(os.path.abspath("../"))
import lib.ISEsettings

ersUsername = lib.ISEsettings.ersUsername
ersPassword = lib.ISEsettings.ersPassword
host = lib.ISEsettings.host
xlsx_path = lib.ISEsettings.xlsx_path
sheet_name = lib.ISEsettings.nas_sheet_name
auth = lib.ISEsettings.auth
Headers = lib.ISEsettings.Headers
network_device_url = lib.ISEsettings.NetworkDeviceURL


# @pysnooper.snoop(prefix="nas_generated_data: ")
def nas_generated_data(sheet_name):
    r = generated_data(sheet_name)
    device_group_dict = {}
    for i in range(0, len(r)):
        device_group_str = str(r[i]["设备Group"]).replace("=", ",")
        device_group_list = str(device_group_str).split(",")
        for index, value in enumerate(device_group_list):
            if index % 2 == 0:
                device_group_dict[value] = device_group_list[index + 1]
        r[i]['设备Group'] = device_group_dict.copy()
    return r


# @pysnooper.snoop(prefix="create_nas: ")
@before_end
def create_nas(sheet_name):
    network_devices = nas_generated_data(sheet_name)
    r_sess = requests.session()
    for network_device in network_devices:
        name = network_device['设备名称']
        share_secret = network_device['AuthKey']
        ip = network_device['IP地址']
        device_profile = network_device['设备Profile']
        device_type = str(network_device['设备Group']['DeviceType'])
        ip_sec = network_device['设备Group']['IPSEC']
        location = str(network_device['设备Group']['Location'])
        payload = {
            "NetworkDevice": {
                "name": name,
                "description": "",
                "authenticationSettings": {
                    "radiusSharedSecret": "",
                    "enableKeyWrap": "false",
                    "dtlsRequired": "false",
                    "keyEncryptionKey": "",
                    "messageAuthenticatorCodeKey": "",
                    "keyInputFormat": "ASCII",
                    "enableMultiSecret": "false"
                },
                "tacacsSettings": {
                    "sharedSecret": share_secret,
                    "connectModeOptions": "OFF",
                    "previousSharedSecret": "",
                    "previousSharedSecretExpiry": 0
                },
                "profileName": device_profile,
                "coaPort": 1700,
                "NetworkDeviceIPList": [
                    {
                        "ipaddress": ip,
                        "mask": 32
                    }
                ],
                "NetworkDeviceGroupList": [
                    "Location#{}".format(location),
                    "IPSEC#Is IPSEC Device#{}".format(ip_sec),
                    "Device Type#All Device Types#{}".format(device_type)
                ]
            }
        }
        payload_json = json.dumps(payload)
        r = r_sess.post(network_device_url, auth=auth, headers=Headers, data=payload_json, verify=False, timeout=(3, 5))
        echo_result(network_device['设备名称'], r)


if __name__ == "__main__":
    create_nas(sheet_name)
