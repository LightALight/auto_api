#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/25 23:11
@Author :
@File Name：    base_api.py
@Description :
-------------------------------------------------
"""
import os.path
import traceback
import requests
from common.api.response_validator import ResponseValidator
from common.my_log import my_log


class BaseAPI:

    def __init__(self, api_def_file=None):
        self.api_def_file = api_def_file
        self.session = requests.Session()

    def __to_request(self, method, url, **kwargs):
        """
        发送请求
        :param method: 请求方式
        :param url: 请求路径
        :param kwargs: 请求参数
        :return: ApiResponse
        """
        # 发送请求
        status_code = 0
        content = ''
        check_response = True
        try:
            res = self.session.request(method, url, **kwargs)
            status_code = res.status_code
            try:
                content = res.json()
            except Exception as e:
                my_log.error(e)
                content = res.text
                check_response = False
        except requests.RequestException as e:
            my_log.info('%s%s' % ('RequestException url: ', url))
            my_log.info(e)
        except Exception as e:
            my_log.info('%s%s' % ('Exception url: ', url))
            traceback.print_exc()
            my_log.info(e)
        my_log.info(f"请求URL: {url}")
        my_log.info(f"请求Headers: {kwargs.get('headers', {})}")
        my_log.info(f"请求Body: {kwargs.get('json', {})}")
        my_log.info(f"响应码: {status_code}")
        my_log.info(f"响应体: {content}")
        if check_response and os.path.exists(self.api_def_file):
            result, message = ResponseValidator(
                self.api_def_file).validate_response(
                url, status_code, content)
            assert result, message
        return status_code, content

    def get(self, url, **kwargs):
        return self.__to_request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.__to_request('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self.__to_request('put', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.__to_request('delete', url, **kwargs)

    def patch(self, url, **kwargs):
        return self.__to_request('patch', url, **kwargs)
