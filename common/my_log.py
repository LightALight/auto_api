#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/26 1:04
@Author :
@File Name：    my_log.py
@Description :
-------------------------------------------------
"""
import logging

# 1. 配置日志记录器
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, filename='log.txt')
logger = logging.getLogger()
