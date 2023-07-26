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
import os
import sys
import time
from logging.handlers import RotatingFileHandler


class MyLog:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, set_level="debug",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y%m%d%H.log", time.localtime()),
                 log_path=os.path.join(
                     os.path.dirname(os.path.dirname(__file__)), "static",
                     "log"),
                 use_console=True):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(
            self.level_relations.get(set_level, logging.NOTSET))

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file_path = os.path.join(log_path, log_name)
        file_handler = RotatingFileHandler(log_file_path,
                                           maxBytes=2 * 1024 * 1024,
                                           backupCount=0, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s - %(name)s - line:%(lineno)d - %(levelname)s]: %(message)s"))
        self.logger.addHandler(file_handler)

        if use_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(
                "[%(asctime)s - %(name)s - line:%(lineno)d - %(levelname)s]: %(message)s"))
            self.logger.addHandler(console_handler)

    def __getattr__(self, item):
        # Delegate all other calls to the internal logger.
        return getattr(self.logger, item)

    def __call__(self, msg, level='info', *args, **kwargs):
        func = getattr(self.logger, level, 'info')
        func(msg, *args, **kwargs)


my_log = MyLog(name=__file__)
