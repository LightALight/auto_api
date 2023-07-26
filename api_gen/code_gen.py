#!/usr/bin/env python

"""
-------------------------------------------------
@date：        2023/7/22 19:18
@Author :
@File Name：    code_gen.py
@Description :
-------------------------------------------------
"""
import os.path

from common.file_func import find_files_recursive, create_file_dir, \
    get_file_name, write_to_file_with_suffix, write_file_json
from common.str_func import camel_to_snake
from config.my_config import code_gen_api_dir, code_gen_raw_api_dir, \
    code_gen_api_smoke_dir
from swagger_to_code import SwaggerToCode


class CodeGen():

    def __init__(self):
        self.raw_api_dir = code_gen_raw_api_dir
        self.api_dir = code_gen_api_dir
        self.smoke_dir = code_gen_api_smoke_dir
        self.file_list = []

    def scan_api_file(self):
        self.file_list = find_files_recursive(
            self.raw_api_dir, file_type="json")
        print(f"Found {len(self.file_list)} API files")

    def generate_api(self):
        for file in self.file_list:
            file_dir_name = get_file_name(file).replace(".json", "")
            api_file_dir = os.path.join(
                self.api_dir, camel_to_snake(file_dir_name))
            create_file_dir(api_file_dir)
            smoke_dir = os.path.join(
                self.smoke_dir, camel_to_snake(file_dir_name))
            create_file_dir(smoke_dir)
            content_dict, url_response_dict = SwaggerToCode(
                file).generate_python_code()
            for file_name, content in content_dict.items():
                api_def, smoke_code, smoke_data = content
                write_to_file_with_suffix(
                    os.path.join(
                        api_file_dir,
                        f"{camel_to_snake(file_name)}.py"),
                    api_def)
                smoke_code = smoke_code.replace(
                    "CLASSNAME", f"{camel_to_snake(file_dir_name)}")
                write_to_file_with_suffix(
                    os.path.join(
                        smoke_dir,
                        f"test_{camel_to_snake(file_name)}_api.py"),
                    smoke_code)
                write_to_file_with_suffix(
                    os.path.join(
                        smoke_dir,
                        f"test_{camel_to_snake(file_name)}_data.py"),
                    smoke_data)
                print(f"Generated {file_name}")
            write_file_json(os.path.join(
                api_file_dir,
                f"{camel_to_snake(file_dir_name)}.json"), url_response_dict)

    def run(self):
        self.scan_api_file()
        self.generate_api()


if __name__ == "__main__":
    CodeGen().run()
