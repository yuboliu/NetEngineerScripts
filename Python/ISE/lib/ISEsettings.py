# -*- coding: UTF-8 -*-
# @Time    : 2020/1/2 13:09
# @Author  : 刘钰博
# @E-mail  : lolipop.boy@outlook.com

ersUsername = 'ersadmin'
ersPassword = 'Cisc0117'
host = '10.1.1.66'
port = 9060
xlsx_path = "..\\data\\Data.xlsx"
internal_sheet_name = "InternalUser"
nas_sheet_name = "NAS"
auth = (ersUsername, ersPassword)
the_operation = "delete"
Headers = {"Accept": "application/json", "Content-Type": "application/json"}
InternalUserUrl = 'https://{}:{}/ers/config/internaluser'.format(host, port)
IdentityGroupURL = 'https://{}:{}/ers/config/identitygroup'.format(host, port)
IdentityGroupSearchURL = 'https://{}:{}/ers/config/identitygroup/name'.format(host, port)
NetworkDeviceURL = 'https://{}:{}/ers/config/networkdevice'.format(host, port)
