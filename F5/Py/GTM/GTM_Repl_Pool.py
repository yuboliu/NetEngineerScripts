#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2021/1/30 17:50
"""

import sys
import os
import json
import urllib3
import requests
import argparse
import re

urllib3.disable_warnings()

sys.path.append(os.path.abspath("../"))
from etc.config import *
from lib.lib import GenURL
from lib.lib import log


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-wideip', required=True, type=str, help="输入域名，多个之间使用英文逗号分隔，例如：ibs.bjrcb.com,asgw.bjrcb.com")
    parser.add_argument('-new_ip', required=True, type=str, help="输入要被替换的新 IP 地址")
    parser.add_argument('-log_level', required=False, type=str, choices=['info', 'debug'], default='info')
    args = parser.parse_args()
    opt_wideip = args.wideip
    opt_new_ip = args.new_ip
    opt_log_level = args.log_level
    
    logger = log(opt_log_level, 'GTM_Repl_Pool')
    logger.info("接收到的参数: {}".format(args))
    domain_names = opt_wideip.split(",")
    logger.info("解析到的域名: {}".format(domain_names))

    req_sess = requests.session()
    class_url = GenURL()
    class_url.set_record_type('a')
    GTMs = Pri_GTM
    for domain_name in domain_names:
        for GTM in GTMs:
            class_url.set_host(GTM)
            URL = class_url.get_all_dn_url('/mgmt/tm/gtm/wideip/')
            r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
            dn_dict = r.json()
            if "items" in dn_dict:
                dn_list = dn_dict["items"]
                for dn_origin in dn_list:
                    dn = dn_origin['name']
                    v4_dn.append(dn)
                real_dn = domain_name
                for dn in v4_dn:
                    if real_dn == str.lower(dn):
                        domain_name = dn
                logger.info("转换后的域名 {}".format(v4_dn))
            else:
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
                r_json = r.json()
                logger.debug(r.json)
                print(r_json['pools'])
                if len(r_json['pools']) == 1 and type(r_json['pools'] == list):
                    for pool in r_json["pools"]:
                        pm = (pool["name"])
                        class_url.set_pool_name(pm)
                        # 获取 Pool Member，也就是 server vs
                        URL = class_url.get_poolmem_url('/mgmt/tm/gtm/pool/')
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        logger.debug(r.json)
                        r_json = r.json()
                        # gtmvs 为 pool member
                        gtm_pm = r_json['items']
                        logger.debug("line 91: {}".format(gtm_pm))
                        # 通过 pool member vs 的名字获取 server 名字
                        # if len(gtm_pm) == 1 and type(gtm_pm) == list:
                        #     for gtm_vs in gtm_pm:
                        #         server_name = tuple(gtm_vs['name'].split(':'))[0]
                        #         logger.info("server name: {}".format(server_name))
                        server_name = ""
                        for gtm_vs in gtm_pm:
                            if not server_name:
                                server_name = tuple(gtm_vs['name'].split(':'))[0]
                            if server_name == tuple(gtm_vs['name'].split(':'))[0]:
                                continue
                            else:
                                quit(1)
                                logger.error("pool 关联的 server 为不同的 server")
                        class_url.set_server_name(server_name)
                        URL = class_url.get_server_detail_url('/mgmt/tm/gtm/server/')
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        logger.debug(r.json())
                        server_dict = r.json()
                        del_one_key = ('kind', 'fullPath', 'generation', 'selfLink', 'datacenterReference', 'devicesReference')
                        del_two_key = ('link', 'isSubcollection')
                        del_three_key = ('generation', 'selfLink', 'kind', 'fullPath')
                        del_four_key = ('deviceName', '')
                        for i in del_one_key:
                            server_dict.pop(i, None)
                        for i in del_two_key:
                            del server_dict['virtualServersReference'][i]
                        for i in del_three_key:
                            for j in server_dict['virtualServersReference']['items']:
                                j.pop(i, None)
                        for i in del_four_key:
                            for j in server_dict['addresses']:
                                j.pop(i, None)
                        logger.debug('清理后的 json：{}'.format(server_dict))
                        # server_dict['name'] = str(server_name['name']) + 'Create_by_Python'
                        for i in server_dict['addresses']:
                            i['name'] = opt_new_ip
                        for i in server_dict['virtualServersReference']['items']:
                            str_dest = str(i['destination'])
                            logger.debug("gtmvs destination is: {}".format(str_dest))
                            server_address = tuple(str_dest.split(':'))[0]
                            str_dest = str_dest.replace(server_address, opt_new_ip)
                            i['destination'] = str_dest
                            i['name'] = str(i['name']) + '_Create_by_Python'
                        server_dict['name'] = str(server_dict['name']) + '_Create_by_Python'
                        logger.debug('修改后的 json：{}'.format(server_dict))
                        URL = class_url.get_all_server_url('/mgmt/tm/gtm/server/')
                        logger.debug(URL)
                        r = req_sess.post(URL, auth=auth, headers=Headers, data=json.dumps(server_dict), verify=False, timeout=(3, 5))
                        logger.info("克隆 Server 的结果为 {}".format(r.status_code))

                        URL = class_url.get_poolmem_detail_url('/mgmt/tm/gtm/pool/')
                        logger.debug("line 150: {}".format(URL))
                        r = req_sess.get(URL, auth=auth, headers=Headers, verify=False, timeout=(3, 5))
                        r_dict = r.json()
                        logger.debug("line 153: {}".format(r_dict))
                        members = r_dict['membersReference']
                        for i in del_two_key:
                            members.pop(i, None)
                        for i in del_three_key:
                            for j in members['items']:
                                j.pop(i, None)
                        pool_member = members['items']
                        for i in pool_member:
                            server_name = tuple(i['name'].split(':'))[0]
                            vs_name = tuple(i['name'].split(':'))[1]
                            i['name'] = server_name + '_Create_by_Python' + ':' + vs_name + '_Create_by_Python'
                            logger.debug("{}".format(i['name']))
                        logger.debug("line 166: {}".format(pool_member))
                        gtm_pool_repl_server['membersReference']['items'] = pool_member
                        r = req_sess.patch(URL, auth=auth, headers=Headers, data=json.dumps(gtm_pool_repl_server), verify=False, timeout=(3, 5))
                        logger.debug(r.json())





