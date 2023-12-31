#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/24 0:33
@Author :
@File Name：    response_validator.py
@Description :
-------------------------------------------------
"""
from common.file_func import read_file_json


class ResponseValidator:

    def __init__(self, config_file):
        # 你提供的校验格式
        self.validation_map = read_file_json(config_file)

    def validate_response(self, url, status_code, response_content):
        # 解析URL，去掉域名
        path = url.split('://')[-1].split('/', 1)[-1]
        segments = path.split('/')

        max_attempts = 3
        attempts = 0
        validation_details = {}

        # 循环尝试获取验证内容
        while attempts < max_attempts and segments:
            relative_url = '/' + '/'.join(segments)
            validation_details = self.validation_map.get(relative_url, {}).get(
                str(status_code), {})
            if validation_details:
                break
            segments.pop(0)
            attempts += 1

        if not validation_details:
            return False, "No validation rules found for this URL and status code"

        properties = validation_details.get("properties", {})
        return self._validate_properties(properties, response_content)

    def _validate_properties(self, properties, content):
        for prop_name, prop_details in properties.items():
            if prop_details.get("required", 1) and prop_name not in content:
                return False, f"Property {prop_name} is required but not found"

            if prop_name in content:
                if prop_details["type"] != type(
                        content[prop_name]).__name__.lower():
                    return False, f"Property {prop_name} is of incorrect type"

                if prop_details.get(
                        'value') and content[prop_name] not in prop_details['value']:
                    return False, f"Property {prop_name} has invalid value"

                if prop_details["type"] == "object":
                    nested_properties = prop_details.get("properties", {})
                    valid, message = self._validate_properties(
                        nested_properties, content[prop_name])
                    if not valid:
                        return False, message

        return True, "Response is valid"
