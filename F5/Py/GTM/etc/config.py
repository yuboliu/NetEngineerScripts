#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/12/27 15:17
"""

from lib.lib import Vividict
d = Vividict()

LoginUser = "admin"
LoginPass = "admin"
auth = (LoginUser, LoginPass)
Headers = {"Accept": "application/json", "Content-Type": "application/json"}
Pub_GTM = ['10.1.1.66']
Pri_GTM = ['10.1.1.66']
# Pri_GTM = ['10.1.1.66', '10.1.1.67']
# Pub_GTM = ['10.1.1.66', '10.1.1.67']
GTM_CM = {'10.1.1.66': "device_trust_group"}
Disabled_JSON = '{"disabled": true}'
Enabled_JSON = '{"enabled": true}'
need_sync = False
v4_dn = []
v6_dn = []
gtm_pool_repl_server = {
  "membersReference": {
    "items": [
    ]
  }
}

ip = {
    'cw': [
        "211.146.16.0/24"
    ],
    'cu': [
        '210.13.250.0/24'
    ],
    'cmcc': [
        '223.72.156.0/24'
    ],
    'ct': [
        '36.112.108.66'
    ],
    'dc': [
        '11.156.0.0/16',
        '11.157.0.0/16'
    ],
    'dr': [
        '11.158.0.0/16',
        '11.159.0.0/16'
    ]
}
associate_f5_with_mgtip = {
    'DC_INTER_LLB4600_01': [
        "1.1.1.1"
    ],
    'DC_INTER2_LLB4600_01': [
        "2.2.2.2"
    ],
    'DR_INTER_LLB4600_01': [
        '10.1.1.66'
    ],
    'DC_PRD_LLB4600_01': [
        '11.156.0.0',
        '11.157.0.0'
    ]
}
d['dc_inter_01']['DC_INTER_LLB4600_01'] = ['211.146.16.0/24', '1.202.134.128/26']
d['dc_inter_02']['DC_INTER2_LLB4600_01'] = ["211.146.16.64/26", "36.112.108.64/26"]
d['dr_inter']['DR_INTER_LLB4600_01'] = ['210.13.250.0/26', '223.72.156.64/26']
d['dc_prd_01']['DC_PRD_LLB4600_01'] = ['11.158.0.0/16', '11.159.0.0/16']

if __name__ == "__main__":
    pass
