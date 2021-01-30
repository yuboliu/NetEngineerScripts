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

sys.path.append(os.path.abspath("../"))
from etc.config import *
from lib.lib import GenURL
from lib.lib import log

urllib3.disable_warnings()
Count_by_Oper_DNS = 0
Count_by_Oper_LTMVS = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-action', required=True, type=str, choices=['active', 'deactive'], help="open = 打开Pool下的vs，close = 关闭Pool下的VS")
    parser.add_argument('-wideip', required=True, type=str, help="输入域名，多个之间使用英文逗号分隔，例如：ibs.bjrcb.com,asgw.bjrcb.com")
    parser.add_argument('-gtm_id', required=True, type=str, choices=['cw', 'cmcc', 'ct', 'cu', 'dc', 'dr'], help="输入定位pool下vs的唯一标识符，例如：'ct'表示pool下vs中名字有包含ct的。该匹配不区分大小写")
    parser.add_argument('-force_usage_pri', action='store_true', help="强制使用内网GTM")
    parser.add_argument('-skip_sync', action='store_true', help="跳过同步配置，默认为是", default=True)
    parser.add_argument('-skip_ipv6', action='store_true', help="跳过ipv6域名，默认为否", default=False)
    parser.add_argument('-log_level', required=False, type=str, choices=['info', 'debug'], default='info')
    parser.add_argument('-is_clear', action='store_true', help="是否清除连接表，默认为否", default=False)
    parser.add_argument('-record_type', required=False, type=str, choices=['v4', 'v6', 'all'], default='all')
    args = parser.parse_args()
    opt_action = args.action
    opt_wideip = args.wideip
    opt_gtm_id = args.gtm_id
    opt_force_pri = args.force_usage_pri
    opt_skip_sync = args.skip_sync
    skip_v6 = args.skip_ipv6
    opt_log_level = args.log_level
    opt_record_type = args.record_type
    opt_is_clear = args.is_clear

    logger = log(opt_log_level, 'GTM_Oper_VS')
    logger.info("接收到的参数: {}".format(args))
    domain_names = opt_wideip.split(",")
    logger.info("解析到的域名: {}".format(domain_names))

    action = Disabled_JSON if opt_action == "deactive" else Enabled_JSON
    logger.info(action)

    if args.record_type == 'v4':
        record_types = ['a']
    elif args.record_type == 'v6':
        record_types = ['aaaa']
    elif args.record_type == 'all':
        record_types = ['a', 'aaaa']

    req_sess = requests.session()
    class_url = GenURL()
    for domain_name in domain_names:
        # record_types = ["a", "aaaa"]
        for record_type in record_types:
            class_url.set_record_type(record_type)
            if skip_v6 and record_type == 'aaaa':
                logger.info("当前域名 {} 不执行IPv6 操作".format(domain_name))
                break
            if opt_force_pri or re.search('int-bjrcb', domain_name, flags=re.I):
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
                    Count_by_Oper_DNS += 1
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
                device_id = ""
                for k, v in d.items():
                    for k2, v2 in v.items():
                        # print(k)
                        # print(k2, v2)
                        for i in v2:
                            r = ipaddress.ip_address(finnal_vsip) in ipaddress.ip_network(i)
                            if r:
                                logger.debug("{}{}{}".format(finnal_vsip, k, v))
                                logger.info("vsip {} 所属的 GTM 标识为 '{}' 所属的地址段 {}".format(finnal_vsip, k, v))
                                logger.info("设备标识符：{}".format(k2))
                                device_id = k2
                            # else:
                            #     logger.info("该地址 {} 不是 VS地址".format(finnal_vsip))
                # 通过设备标识符获取设备登录地址
                if device_id:
                    for mgtip in associate_f5_with_mgtip[device_id]:
                        logger.info("通过vsip查询到的 LTM 登录地址为：{}".format(mgtip))
                        URL = class_url.get_sys_failver_url('/mgmt/tm/sys/failover/')
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        r_dict = json.loads(r.text)
                        logger.info(r_dict['apiRawValues']['apiAnonymous'])
                        r = re.search('Failover active', r_dict['apiRawValues']['apiAnonymous'], flags=re.I)
                        if r:
                            isgoon = 1
                            break
                else:
                    logger.error("未能通过vsip定位到关联的 LTM")
                    quit(1)
                if not isgoon:
                    logger.error("未能在 {} 里找到 active 设备".format(device_id))
                    quit(1)
                # 通过 finnal_vsip 获取到 ltm 上面的 vs name
                ltmvs_name = []
                URL = class_url.get_all_ltmvs_url('/mgmt/tm/ltm/virtual/')
                r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                r_dict = json.loads(r.text)
                all_ltmvs_list = r_dict['items']
                for ltmvs in all_ltmvs_list:
                    r = re.search(finnal_vsip, ltmvs['destination'])
                    if r:
                        ltmvs_name.append(ltmvs['name'])
                if not ltmvs_name:
                    logger.error("未能通过finnal_vsip 找到关联的vs name")
                    quit(1)
                logger.info("通过 finnal_vsip 找到关联的 LTM vs name 为{}".format(ltmvs_name))
                # 关闭 ltmvs
                for ltmvs in ltmvs_name:
                    URL = class_url.get_ltmvs_url('/mgmt/tm/ltm/virtual', ltmvs)
                    logger.debug(URL)
                    r = req_sess.patch(URL, auth=auth, headers=Headers, data=action, verify=False, timeout=(3, 5))
                    logger.info("修改vs {} 状态返回的结果为: {}".format(ltmvs, r.text))
                    Count_by_Oper_LTMVS += 1
                # 清除 LTM sys connecting
                if opt_is_clear:
                    URL = class_url.get_ltm_sys_conn_url('/mgmt/tm/sys/connection?options=cs-server-addr', finnal_vsip)
                    logger.debug(URL)
                    r = req_sess.delete(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                    logger.info("删除 LTM sys conn 的结果为: {}".format(r.text))

    if need_sync and not opt_skip_sync:
        for GTM in Pri_GTM:
            # 执行 save sys config
            # r = req_sess.post("https://{}/mgmt/tm/sys/config".format(GTM), data='{"command" : "save"}', auth=auth, headers=Headers, verify=False)
            # 执行 run cm config-sync to-group
            CmdArgs = "config-sync to-group {}".format(GTM_CM['{}'.format(GTM)])
            payload = {"command": "run", "utilCmdArgs": CmdArgs}
            r = req_sess.post("https://{}/mgmt/tm/cm".format(GTM), data=json.dumps(payload), auth=auth, headers=Headers, verify=False)
    logger.info("共执行 {} 次 DNS 操作".format(Count_by_Oper_DNS))
    logger.info("共执行 {} 次 LTMVS 操作".format(Count_by_Oper_LTMVS))
