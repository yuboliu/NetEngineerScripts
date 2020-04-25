#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: 刘钰博
@Contact: lolipop.boy@outlook.com
@Time: 2020/4/25 9:15
"""

import sys
import os
import logging
sys.path.append(os.path.abspath("../"))


def log():
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('..\\log\\{0}.log'.format(today))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    pass
