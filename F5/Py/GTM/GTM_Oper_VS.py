#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/11/22 10:30
"""

import sys
import os
import requests
import json
import re
import urllib3
import argparse
urllib3.disable_warnings()


LoginUser = "admin"
LoginPass = "admin"
auth = (LoginUser, LoginPass)
Headers = {"Accept": "application/json", "Content-Type": "application/json"}
Pri_GTM = ['10.1.1.66']
Pub_GTM = ['10.1.1.66']
Disabled_JSON = '{"disabled": true}'
Enabled_JSON = '{"enabled": true}'


def log(level):
    import logging
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    go_level = {"info": logging.INFO, "error": logging.ERROR, "debug": logging.DEBUG, "warning": logging.WARNING, "critical": logging.CRITICAL}
    logger = logging.getLogger()
    logger.setLevel(go_level[level])
    # fh = logging.FileHandler('..\\log\\{0}.log'.format(today))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    logger = log("info")

    parser = argparse.ArgumentParser()
    parser.add_argument('-action', required=True, type=str, choices=['open', 'close'])
    parser.add_argument('-wideip', required=True, type=str)
    parser.add_argument('-gtm_id', required=True, type=str, choices=['cw', 'cmcc'])
    args = parser.parse_args()
    opt_action = args.action
    opt_wideip = args.wideip
    opt_gtm_id = args.gtm_id
    logger.info("接收到的参数: {}".format(args))
    domain_names = opt_wideip.split(",")
    logger.info("解析到的域名: {}".format(domain_names))
    action = Disabled_JSON if opt_action == "close" else Enabled_JSON

    for domain_name in domain_names:
        record_types = ["a", "aaaa"]
        skip_ipv6 = False
        for record_type in record_types:
            if skip_ipv6:
                break
            if re.search('int-bjrcb', domain_name, flags=re.I):
                GTMs = Pri_GTM
                skip_ipv6 = True
            else:
                GTMs = Pub_GTM
            logger.info("当前域名: {}，是否跳过IPv6: {}".format(domain_name, skip_ipv6))
            for GTM in GTMs:
                logger.info("当前GTM地址: {}".format(GTM))
                URI = "/mgmt/tm/gtm/wideip/{}/{}".format(record_type, domain_name)
                URL = "https://{}{}".format(GTM, URI)
                req_sess = requests.session()
                r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                r.raise_for_status()
                r_json = r.json()
                for pool in r_json["pools"]:
                    pm = (pool["name"])
                    URI = "/mgmt/tm/gtm/pool/{}/{}/members".format(record_type, pm)
                    URL = "https://{}{}".format(GTM, URI)
                    r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                    r_json = r.json()
                    for vs in r_json["items"]:
                        match = re.search(opt_gtm_id, vs["name"], flags=re.I)
                        if match:
                            URI = "/mgmt/tm/gtm/pool/{}/{}/members/~Common~{}".format(record_type, pm, vs["name"])
                            URL = "https://{}{}".format(GTM, URI)
                            r = req_sess.patch(URL, auth=auth, headers=Headers, data=action, verify=False, timeout=(3, 5))
                            logger.info("返回结果为: {}".format(r_json))
                logger.info("=====================--------------我是华丽的分割线--------------=====================")
