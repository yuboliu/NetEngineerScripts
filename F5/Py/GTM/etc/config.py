#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/12/27 15:17
"""

LoginUser = "admin"
LoginPass = "admin"
auth = (LoginUser, LoginPass)
Headers = {"Accept": "application/json", "Content-Type": "application/json"}
Pri_GTM = ['10.1.1.66', '10.1.1.67']
# Pub_GTM = ['10.1.1.66', '10.1.1.67']
GTM_CM = {'10.1.1.66': "device_trust_group"}
Pub_GTM = ['10.1.1.66']
Disabled_JSON = '{"disabled": true}'
Enabled_JSON = '{"enabled": true}'
need_sync = False
# skip_ipv6 = False
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
associate_vsip_with_slb = {
    '亦庄': [
        "211.146.16.0/24",
        '36.112.108.66'
    ],
    '空港': [
        '210.13.250.0/24',
        '223.72.156.0/24'
    ],
    '业务二区': [
        '11.156.0.0/16',
        '11.157.0.0/16'
    ],
    '业务三区': [
        '11.158.0.0/16',
        '11.159.0.0/16'
    ]
}
associate_slb_mgt_ip = {
    '空港': [
        '10.1.1.66'
    ]
}

if __name__ == "__main__":
    pass
