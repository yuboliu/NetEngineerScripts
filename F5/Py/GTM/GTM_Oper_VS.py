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
# import ipaddr
import ipaddress
urllib3.disable_warnings()


LoginUser = "admin"
LoginPass = "admin"
auth = (LoginUser, LoginPass)
Headers = {"Accept": "application/json", "Content-Type": "application/json"}
Pri_GTM = ['10.1.1.66']
Pub_GTM = ['10.1.1.66']
Disabled_JSON = '{"disabled": true}'
Enabled_JSON = '{"enabled": true}'
need_sync = False
GTM_CM = {'10.1.1.66': "device_trust_group"}
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


class GenURL:
    def __init__(self):
        self.record_type = '/'
        self.domain_name = '/'
        self.server_name = '/'
        self.host = '/'
        self.pool_name = '/'

    def set_record_type(self, record_type):
        self.record_type = record_type

    def set_domain_name(self, domain_name):
        self.domain_name = domain_name

    def set_server_name(self, server_name):
        self.server_name = server_name

    def set_host(self, host):
        self.host = host

    def set_pool_name(self, pool_name):
        self.pool_name = pool_name

    def get_wideip_url(self, uri_prefix):
        return "https://{}{}{}/{}".format(self.host, uri_prefix, self.record_type, self.domain_name)

    def get_server_url(self, uri_prefix):
        return "https://{}{}~Common~{}".format(self.host, uri_prefix, self.server_name)

    def get_vs_detail_url(self, uri_prefix, vs_name):
        return 'https://{}{}{}/{}/members/~Common~{}'.format(self.host, uri_prefix, self.record_type, self.pool_name, vs_name)

    def get_poolmem_url(self, uri_prefix):
        return "https://{}{}{}/{}/members".format(self.host, uri_prefix, self.record_type, self.pool_name, self.server_name)


if __name__ == "__main__":
    logger = log("debug")

    parser = argparse.ArgumentParser()
    parser.add_argument('-action', required=True, type=str, choices=['active', 'deactive'], help="open = 打开Pool下的vs，close = 关闭Pool下的VS")
    parser.add_argument('-wideip', required=True, type=str, help="输入域名，多个之间使用英文逗号分隔，例如：ibs.bjrcb.com,asgw.bjrcb.com")
    parser.add_argument('-gtm_id', required=True, type=str, choices=['cw', 'cmcc', 'ct', 'cu', 'dc', 'dr'], help="输入定位pool下vs的唯一标识符，例如：'ct'表示pool下vs中名字有包含ct的。该匹配不区分大小写")
    parser.add_argument('-force_usage_pri', action='store_true', help="强制使用内网GTM")
    parser.add_argument('-skip_sync', action='store_true', help="跳过同步配置")
    parser.add_argument('-skip_ipv6', action='store_true', help="跳过ipv6域名")
    args = parser.parse_args()
    opt_action = args.action
    opt_wideip = args.wideip
    opt_gtm_id = args.gtm_id
    opt_force = args.force_usage_pri
    opt_skip_sync = args.skip_sync
    opt_skip_v6 = args.skip_ipv6
    logger.info("接收到的参数: {}".format(args))
    domain_names = opt_wideip.split(",")
    logger.info("解析到的域名: {}".format(domain_names))

    action = Disabled_JSON if opt_action == "deactive" else Enabled_JSON
    logger.debug(action)

    req_sess = requests.session()
    class_url = GenURL()
    for domain_name in domain_names:
        record_types = ["a", "aaaa"]
        skip_ipv6 = False
        print(skip_ipv6)
        for record_type in record_types:
            class_url.set_record_type(record_type)
            if skip_ipv6:
                break
            if opt_force or re.search('int-bjrcb', domain_name, flags=re.I) or opt_skip_v6:
                GTMs = Pri_GTM
                skip_ipv6 = True
                need_sync = True
            else:
                GTMs = Pub_GTM
            logger.info("当前域名: {}，是否跳过IPv6: {}".format(domain_name, skip_ipv6))
            for GTM in GTMs:
                class_url.set_host(GTM)
                logger.info("当前GTM地址: {}".format(GTM))
                # URI = "/mgmt/tm/gtm/wideip/{}/{}".format(record_type, domain_name)
                # URL = "https://{}{}".format(GTM, URI)
                class_url.set_domain_name(domain_name)
                URL = class_url.get_wideip_url('/mgmt/tm/gtm/wideip/')
                r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                r.raise_for_status()
                r_json = r.json()
                for pool in r_json["pools"]:
                    pm = (pool["name"])
                    # URI = "/mgmt/tm/gtm/pool/{}/{}/members".format(record_type, pm)
                    # URL = "https://{}{}".format(GTM, URI)
                    class_url.set_pool_name(pm)
                    URL = class_url.get_poolmem_url('/mgmt/tm/gtm/pool/')
                    r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                    r_json = r.json()
                    vs_addrs = []
                    for vs in r_json["items"]:
                        server_name = tuple(vs['name'].split(':'))[0]
                        # URI = "/mgmt/tm/gtm/server/~Common~{}".format(server_name)
                        # URL = "https://{}{}".format(GTM, URI)
                        class_url.set_server_name(server_name)
                        URL = class_url.get_server_url('/mgmt/tm/gtm/server/')
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        r_dict = json.loads(r.text)
                        vs_addrs_dict = r_dict['addresses']
                        for i in vs_addrs_dict:
                            vs_ip = i['name']
                            subs = ip[opt_gtm_id]
                            for sub in subs:
                                import ipaddr
                                # new_net = ipaddr.IPNetwork(one_ip)
                                # old_net = ipaddr.IPNetwork(sub)
                                # r = new_net.overlaps(old_net)
                                r = ipaddress.ip_address(vs_ip) in ipaddress.ip_network(sub)
                                if r:
                                    # URI = "/mgmt/tm/gtm/pool/{}/{}/members/~Common~{}".format(record_type, pm, vs["name"])
                                    # URL = "https://{}{}".format(GTM, URI)
                                    logger.debug("{} # {}".format(vs_ip, sub))
                                    URL = class_url.get_vs_detail_url('/mgmt/tm/gtm/pool/', vs['name'])
                                    logger.debug(URL)
                                    r = req_sess.patch(URL, auth=auth, headers=Headers, data=action, verify=False, timeout=(3, 5))
                                    logger.debug("修改vs状态返回的结果为: {}".format(r.json()))
                logger.info("=====================--------------我是华丽的分割线--------------=====================")
    if need_sync and not opt_skip_sync:
        for GTM in Pri_GTM:
            # r = req_sess.post("https://{}/mgmt/tm/sys/config".format(GTM), data='{"command" : "save"}', auth=auth, headers=Headers, verify=False)
            CmdArgs = "config-sync to-group {}".format(GTM_CM['{}'.format(GTM)])
            payload = {"command": "run", "utilCmdArgs": CmdArgs}
            r = req_sess.post("https://{}/mgmt/tm/cm".format(GTM), data=json.dumps(payload), auth=auth, headers=Headers, verify=False)
