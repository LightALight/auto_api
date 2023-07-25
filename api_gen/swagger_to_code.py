#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/23 10:15
@Author :
@File Name：    swagger_to_code.py
@Description :
-------------------------------------------------
"""

import json

from common.str_func import camel_to_snake, type_java_to_python


class SwaggerToCode():

    def __init__(self, swagger_json_path):
        with open(swagger_json_path, 'r',
                  encoding='utf-8') as f:
            self.swagger_json = json.load(f)

    def generate_python_code(self):
        swagger_json = self.swagger_json
        # api_info = swagger_json["info"]
        base_path = swagger_json["basePath"]
        paths = swagger_json["paths"]
        class_dict = {tag['name']: [] for tag in swagger_json["tags"]}

        # 对每个url进行分类
        for path, methods in paths.items():
            for method, details in methods.items():
                # 生成类定义
                tag = details["tags"][0]  # 这里我们只取第一个标签作为类名
                if tag not in class_dict.keys():
                    class_dict[tag] = []
                else:
                    class_dict[tag].append([path, method, details])

        # 对每个类进行处理
        class_code_dict = dict()
        url_total_response_dict = dict()
        for tag, paths in class_dict.items():
            class_desc = tag
            class_name = ""
            class_url_list = []
            for path in paths:
                url_dict = dict()
                url = path[0]
                url_dict['url'] = url
                url_dict['method'] = path[1]
                detail_dict = path[2]
                if not class_name:
                    parts = url.split("/")
                    if len(parts) >= 3:
                        class_name = parts[2].title() + parts[1].title()
                    else:
                        raise Exception(
                            f"Error: Could not generate class name for {url}: ")
                for key, value in detail_dict.items():
                    if key == "summary":
                        url_dict["url_desc"] = value
                    elif key == "consumes":
                        url_dict["url_content_type"] = value[0]
                    elif key == "parameters":
                        # 对于每个参数，生成参数定义
                        parameter_dict = value[0]

                        if parameter_dict['in'] == "body":
                            param_def_dict = dict()
                            schema = parameter_dict['schema']
                            required_list = schema['required']
                            properties_dict = schema[
                                'properties']
                            if schema['type'] == "object":
                                for prop_name, prop_details in properties_dict.items():
                                    new_prop_details = dict()
                                    if prop_details['type'] == "object":
                                        new_prop_details['properties'] = prop_details['properties']
                                    else:
                                        raise Exception(
                                            "Error: Could not generate body ")
                                    if prop_name in required_list:
                                        new_prop_details["required"] = 1
                                    else:
                                        new_prop_details["required"] = 0
                                    param_def_dict[prop_name] = new_prop_details

                            else:
                                raise Exception(
                                    "Error: Could not generate body ")

                        else:
                            raise Exception(
                                "Error: Could not generate params ")

                        url_dict["url_input_parameter_dict"] = param_def_dict

                    elif key == "responses":
                        response_dict = value
                        url_response_dict = dict()
                        for status_code, response_details in response_dict.items():
                            status_code_dict = dict()
                            status_code_dict["status_desc"] = response_details["description"]
                            schema = response_details["schema"]
                            required_list = schema["required"]
                            if schema["type"] == "object":
                                properties_dict = schema["properties"]
                                for prop_name, prop_details in properties_dict.items():
                                    prop_details['type'] = type_java_to_python(
                                        prop_details['type'])
                                    if prop_name in required_list:
                                        prop_details["required"] = 1
                                    else:
                                        prop_details["required"] = 0
                                status_code_dict["properties"] = properties_dict
                            else:
                                raise Exception(
                                    "Error: Could not generate response ")
                            url_response_dict[status_code] = status_code_dict
                        url_total_response_dict[url] = url_response_dict
                class_url_list.append(url_dict)
            # 开始生成Python代码
            code = []
            code.append("import os")
            code.append("import requests")
            code.append(
                "from common.api.response_validator import ResponseValidator")
            code.append("from common.file_func import get_file_dir")
            code.append(f"class {class_name}:")
            code.append(f'    """')
            code.append(f'    {class_desc}')
            code.append(f'    """')

            # 基础URL定义
            code.append(
                f"    BASE_URL = '{base_path}'  # TODO: Update with actual base URL")
            code.append(
                f"    headers = dict()  # TODO: Update with actual headers URL")
            code.append(
                f"    validator = ResponseValidator(os.path.join(get_file_dir(__file__), '{camel_to_snake(class_name)}.json'))")

            # 开始生成冒烟代码
            smoke_code = []
            smoke_code.append("import pytest as pytest")
            smoke_code.append("import allure")
            smoke_code.append(
                f"from common.api.CLASSNAME.{camel_to_snake(class_name)} import {class_name}")
            smoke_code_def = []
            smoke_code_def.append(f"@pytest.mark.{class_desc}")
            smoke_code_def.append(f"class Test{class_name}:")
            smoke_data = []

            # 方法定义
            for index, class_url in enumerate(class_url_list):
                path = class_url['url']
                method = class_url['method']
                func_desc = class_url['url_desc']
                content_type = class_url['url_content_type']
                param_def_dict = class_url['url_input_parameter_dict']

                func_name_list = path.split("/")
                func_name_list.insert(0, method)
                func_name = "_".join([camel_to_snake(func_name.replace("-", "_"))
                                      for func_name in func_name_list if func_name])
                param_def_list = []
                param_def_desc_list = []
                param_input_list = []
                for param_name, param_details in param_def_dict.items():
                    if param_details["properties"]:
                        param_input_list.append(f'"{param_name}": ' + "{")
                        for sub_param_name, sub_param_details in param_details["properties"].items(
                        ):
                            param_input_list.append(
                                f'"{sub_param_name}": {camel_to_snake(sub_param_name)},')
                            example = sub_param_details.get(
                                'example', '') or sub_param_details.get(
                                'minimum', '')
                            param_def_desc_list.append(
                                f"        :param {camel_to_snake(sub_param_name)}: {sub_param_details.get('description')} 如:{example}")
                            if sub_param_details.get('properties'):
                                for sub_sub_param_name, sub_sub_param_details in \
                                        sub_param_details["properties"].items(
                                        ):
                                    param_def_desc_list.append(
                                        f"                    {sub_sub_param_name}: {type_java_to_python(sub_sub_param_details.get('type'))} {sub_sub_param_details.get('description')}")
                            if sub_param_details.get('required', 1):
                                param_def_list.append(
                                    f"{camel_to_snake(sub_param_name)}: {type_java_to_python(sub_param_details.get('type'))}")
                            else:
                                param_def_list.append(
                                    f"{camel_to_snake(sub_param_name)}=None : {type_java_to_python(sub_param_details.get('type'))}")

                        param_input_list.append("},")
                    else:
                        param_input_list.append(
                            f'"{param_name}": {camel_to_snake(param_name)},')
                        example = param_details.get(
                            'example', '') or param_details.get('minimum', '')
                        param_def_desc_list.append(
                            f"        :param {camel_to_snake(param_name)}: {param_details.get('description')} 如:{example}")
                        if param_details.get('properties'):
                            for sub_param_name, sub_param_details in \
                                    param_details["properties"].items():
                                param_def_desc_list.append(
                                    f"                    {sub_param_name}: {type_java_to_python(sub_param_details.get('type'))} {sub_param_details.get('description')}")
                        if param_details.get('required', 1):
                            param_def_list.append(
                                f"{camel_to_snake(param_name)}: {type_java_to_python(param_details.get('type'))}")
                        else:
                            param_def_list.append(
                                f"{camel_to_snake(param_name)}=None : {type_java_to_python(param_details.get('type'))}")

                smoke_code.append(f'from testcases.test_smoke.CLASSNAME.test_{camel_to_snake(class_name)}_data import test_{func_name}_case_data')
                smoke_code_def.append(f"    @allure.description(u'{func_desc}')")
                smoke_code_def.append(f"    @allure.story(u'{func_desc}')")
                smoke_code_def.append(f"    @allure.title(u'{func_desc}')")
                smoke_code_def.append(f"    @pytest.mark.{func_desc}")
                smoke_code_def.append(
                    f"    @pytest.mark.parametrize('case_data', test_{func_name}_case_data)")
                smoke_code_def.append(
                    f"    def test_{func_name}(self, case_data):")
                smoke_code_def.append(
                    f"        {class_name}().{func_name}(**case_data)")
                smoke_code_def.append("")

                smoke_data.append(
                    f"test_{func_name}_case_data = []")
                smoke_data.append("")

                code.append(
                    f"    def {func_name}(self, {', '.join(param_def_list)}):")
                code.append(f'        """')
                code.append(f"        {func_desc}")
                for param_def_desc in param_def_desc_list:
                    code.append(param_def_desc)
                code.append(f'        """')
                code.append(f'        url = self.BASE_URL + "{path}"')
                code.append(
                    f'        self.headers["Content-Type"] = "{content_type}"')
                code.append(f'        body = ' + '{')
                for param_input in param_input_list:
                    code.append(f"        {param_input}")
                code.append('        }')
                code.append(
                    f"        response = requests.{method}(url, headers=self.headers, json=body)")
                code.append("        try:")
                code.append(
                    "            result, message = self.validator.validate_response(url, response.status_code, response.json())")
                code.append("            assert result, message")
                code.append("        except Exception as e:")
                code.append("            print(e)")
                code.append(
                    "        return response.status_code, response.json()")
                code.append("")

            smoke_code += smoke_code_def
            if class_name in class_code_dict.keys():
                class_name = f"{class_name}Second"

            class_code_dict[class_name] = [
                "\n".join(code),
                "\n".join(smoke_code),
                "\n".join(smoke_data)]
        return class_code_dict, url_total_response_dict


if __name__ == "__main__":
    pass
