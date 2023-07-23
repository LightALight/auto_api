#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/23 15:39
@Author :
@File Name：    str_func.py
@Description :
-------------------------------------------------
"""


import re


def camel_to_snake(name):
    # 一个简单的camel到snake的转换函数
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

def type_java_to_python(j_type):
    # 假设的Java到Python类型转换函数
    return {
        'object': 'dict',
        'array': 'list',
        'string': 'str',
        'integer': 'int',
        'float': 'float',
        'boolean': 'bool',
        # 添加更多映射
    }.get(j_type, 'Any')


if __name__ == "__main__":
    print(camel_to_snake("helloWorld"))
