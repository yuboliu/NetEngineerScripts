#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2021/1/30 17:58
"""


def log(level, py_name):
    import logging
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    go_level = {"info": logging.INFO, "error": logging.ERROR, "debug": logging.DEBUG, "warning": logging.WARNING, "critical": logging.CRITICAL}
    logger = logging.getLogger()
    logger.setLevel(go_level[level])
    # fh = logging.FileHandler('..\\log\\{0}{1}.log'.format(py_name, today))
    fh = logging.FileHandler('log/{0}{1}.log'.format(py_name, today))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
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

    def get_all_server_url(self, uri_prefix):
        return "https://{}{}".format(self.host, uri_prefix)

    def get_server_detail_url(self, uri_prefix):
        return "https://{}{}~Common~{}?expandSubcollections=true".format(self.host, uri_prefix, self.server_name)

    def get_vs_detail_url(self, uri_prefix, vs_name):
        return 'https://{}{}{}/{}/members/~Common~{}'.format(self.host, uri_prefix, self.record_type, self.pool_name, vs_name)

    def get_poolmem_url(self, uri_prefix):
        return "https://{}{}{}/{}/members".format(self.host, uri_prefix, self.record_type, self.pool_name, self.server_name)

    def get_poolmem_detail_url(self, uri_prefix):
        return "https://{}{}{}/{}/?expandSubcollections=true".format(self.host, uri_prefix, self.record_type, self.pool_name)

    def get_all_dn_url(self, uri_prefix):
        return "https://{}{}{}".format(self.host, uri_prefix, self.record_type)

    def get_sys_failver_url(self, uri_prefix):
        return "https://{}{}".format(self.host, uri_prefix)

    def get_all_ltmvs_url(self, uri_prefix):
        return "https://{}{}".format(self.host, uri_prefix)

    def get_ltmvs_url(self, uri_prefix, vs_name):
        return 'https://{}{}/~Common~{}'.format(self.host, uri_prefix, vs_name)

    def get_ltm_sys_conn_url(self, uri_prefix, ltmvs):
        return 'https://{}{}+{}'.format(self.host, uri_prefix, ltmvs)


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


if __name__ == "__main__":
    pass
