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
import ipaddress
urllib3.disable_warnings()

sys.path.append(os.path.abspath("../"))
from etc.config import *

Count_by_Close = 0
v4_dn = []
v6_dn = []


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

    def get_all_dn_url(self, uri_prefix):
        return "https://{}{}{}".format(self.host, uri_prefix, self.record_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-action', required=True, type=str, choices=['active', 'deactive'], help="open = 打开Pool下的vs，close = 关闭Pool下的VS")
    parser.add_argument('-wideip', required=True, type=str, help="输入域名，多个之间使用英文逗号分隔，例如：ibs.bjrcb.com,asgw.bjrcb.com")
    parser.add_argument('-gtm_id', required=True, type=str, choices=['cw', 'cmcc', 'ct', 'cu', 'dc', 'dr'], help="输入定位pool下vs的唯一标识符，例如：'ct'表示pool下vs中名字有包含ct的。该匹配不区分大小写")
    parser.add_argument('-force_usage_pri', action='store_true', help="强制使用内网GTM")
    parser.add_argument('-skip_sync', action='store_true', help="跳过同步配置", default=True)
    parser.add_argument('-skip_ipv6', action='store_true', help="跳过ipv6域名", default=False)
    parser.add_argument('-log_level', required=False, type=str, choices=['info', 'debug'], default='info')
    args = parser.parse_args()
    opt_action = args.action
    opt_wideip = args.wideip
    opt_gtm_id = args.gtm_id
    opt_force = args.force_usage_pri
    opt_skip_sync = args.skip_sync
    skip_v6 = args.skip_ipv6
    opt_log_level = args.log_level

    logger = log(opt_log_level)
    logger.info("接收到的参数: {}".format(args))
    domain_names = opt_wideip.split(",")
    logger.info("解析到的域名: {}".format(domain_names))

    action = Disabled_JSON if opt_action == "deactive" else Enabled_JSON
    logger.info(action)

    req_sess = requests.session()
    class_url = GenURL()
    for domain_name in domain_names:
        record_types = ["a", "aaaa"]
        for record_type in record_types:
            class_url.set_record_type(record_type)
            if skip_v6 and record_type == 'aaaa':
                logger.info("当前域名 {} 不执行IPv6 操作".format(domain_name))
                break
            if opt_force or re.search('int-bjrcb', domain_name, flags=re.I):
                GTMs = Pri_GTM
                skip_ipv6 = True
                need_sync = True
            else:
                GTMs = Pub_GTM
            logger.info("当前域名: {}，是否跳过IPv6: {}".format(domain_name, skip_v6))
            for GTM in GTMs:
                class_url.set_host(GTM)
                logger.info("当前GTM地址: {}".format(GTM))
                # 将所有GTM上面的域名放入list内。
                if not v4_dn or v4_dn and not v6_dn:
                    URL = class_url.get_all_dn_url('/mgmt/tm/gtm/wideip/')
                    r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                    dn_dict = r.json()
                    if "items" in dn_dict:
                        dn_list = dn_dict["items"]
                        for dn_origin in dn_list:
                            dn = dn_origin['name']
                            if record_type == 'a':
                                v4_dn.append(dn)
                            elif record_type == 'aaaa':
                                v6_dn.append(dn)
                        if record_type == 'a':
                            real_dn = domain_name
                            for dn in v4_dn:
                                if real_dn == str.lower(dn):
                                    domain_name = dn
                            logger.info("转换后的域名 {}".format(v4_dn))
                        elif record_type == 'aaaa':
                            real_dn = domain_name
                            for dn in v6_dn:
                                if real_dn == str.lower(dn):
                                    domain_name = dn
                            logger.info("转换后的域名 {}".format(v6_dn))
                    else:
                        if not v6_dn:
                            logger.info("do not found any ipv6 domain name")
                            quit(1)
                        if not v4_dn:
                            logger.info("do not found any ipv4 domain name")
                            quit(1)
                class_url.set_domain_name(domain_name)
                # 查看特定域名的 wideip 信息
                URL = class_url.get_wideip_url('/mgmt/tm/gtm/wideip/')
                r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                try:
                    r.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    if r.status_code // 404 == 1:
                        logger.info(e)
                        continue
                    else:
                        raise Exception("r.static_code is {}".format(r.status_code))
                else:
                    Count_by_Close += 1
                    r_json = r.json()
                    for pool in r_json["pools"]:
                        pm = (pool["name"])
                        class_url.set_pool_name(pm)
                        URL = class_url.get_poolmem_url('/mgmt/tm/gtm/pool/')
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        r_json = r.json()
                        vs_addrs = []
                        for vs in r_json["items"]:
                            server_name = tuple(vs['name'].split(':'))[0]
                            class_url.set_server_name(server_name)
                            URL = class_url.get_server_url('/mgmt/tm/gtm/server/')
                            r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                            r_dict = json.loads(r.text)
                            vs_addrs_dict = r_dict['addresses']
                            for i in vs_addrs_dict:
                                vs_ip = i['name']
                                subs = ip[opt_gtm_id]
                                for sub in subs:
                                    r = ipaddress.ip_address(vs_ip) in ipaddress.ip_network(sub)
                                    if r:
                                        logger.info("查询到的 VS IP 地址 {} # 所属于已定义的地址段 {}".format(vs_ip, sub))
                                        URL = class_url.get_vs_detail_url('/mgmt/tm/gtm/pool/', vs['name'])
                                        logger.info(URL)
                                        r = req_sess.patch(URL, auth=auth, headers=Headers, data=action, verify=False, timeout=(3, 5))
                                        logger.info("修改vs状态返回的结果为: {}".format(r.json()))
                                        finnal_vsip = vs_ip
                finally:
                    logger.info("=====================--------------完成一次域名操作--------------=====================")
                # 通过VSIP 查询 associate_vsip_with_slb 的标识符
                for k, v in associate_vsip_with_slb.items():
                    for i in v:
                        r = ipaddress.ip_address(finnal_vsip) in ipaddress.ip_network(i)
                        if r:
                            print(finnal_vsip, k, v)
                            logger.info("vsip {} 反查到的 GTM 标识 '{}' 所属的地址段 {}".format(finnal_vsip, k, v))
                        else:
                            logger.info("该地址 {} 不是 VS地址".format(finnal_vsip))


    if need_sync and not opt_skip_sync:
        for GTM in Pri_GTM:
            # r = req_sess.post("https://{}/mgmt/tm/sys/config".format(GTM), data='{"command" : "save"}', auth=auth, headers=Headers, verify=False)
            CmdArgs = "config-sync to-group {}".format(GTM_CM['{}'.format(GTM)])
            payload = {"command": "run", "utilCmdArgs": CmdArgs}
            r = req_sess.post("https://{}/mgmt/tm/cm".format(GTM), data=json.dumps(payload), auth=auth, headers=Headers, verify=False)
    logger.info("共执行 {} 次域名操作".format(Count_by_Close))
