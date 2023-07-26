#!/usr/bin/env python
import os
import pytest
from config.my_config import allure_dir

if __name__ == '__main__':
    '''
    -q: 安静模式, 不输出环境信息
    -v: 丰富信息模式, 输出更详细的用例执行信息
    -s: 显示程序中的print/logging输出
    '''
    pytest.main(['-s',
                 '-q',
                 'testcases/test_smoke/demo/test_confirm_operate.py',
                 '--clean-alluredir',
                 '--alluredir=report/allure-results'])
    os.system(
        f"{allure_dir} generate report/allure-results -o report/allure-report")
    os.system(f"{allure_dir} serve report/allure-results")
