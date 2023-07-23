#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/22 19:19
@Author :
@File Name：    config.py
@Description :
-------------------------------------------------
"""
import os

from common.file_func import get_project_dir

project_dir = get_project_dir()
code_gen_raw_api_dir = os.path.join(project_dir, 'docs', 'api')
code_gen_api_dir = os.path.join(project_dir, 'common', 'api')
code_gen_api_smoke_dir = os.path.join(project_dir, 'testcases', 'test_smoke')
allure_dir = os.path.join(project_dir, 'allure', 'bin', 'allure.bat')
