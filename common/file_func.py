# -*- coding:utf-8 -*-
import json
import os


def read_file_json(filename):
    # 获取文件的目录部分
    directory = os.path.dirname(filename)

    # 如果目录不存在，则创建它
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # 检查文件是否存在
    if os.path.exists(filename):
        try:
            # 尝试打开文件并读取内容
            with open(filename, 'r') as file:
                content = json.load(file)
            return content
        except Exception as e:
            # 如果出现任何错误，打印错误并返回None
            print(f"Error reading file {filename}: {e}")
            return None
    else:
        # 文件不存在，返回False
        return False


def write_file_json(filename, content):
    with open(filename, 'w+') as file:
        json.dump(content, file)


def get_file_name(filename):
    """
    获取文件名
    :param filename:
    :return:
    """
    return os.path.basename(filename)


def get_file_dir(filename):
    """
    获取文件名
    :param filename:
    :return:
    """
    return os.path.dirname(filename)


def create_file_dir(dir_path):
    """
    获取文件名
    :param dir_path:
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_project_dir():
    """
    获取文件名
    :return:
    """
    return os.path.dirname(os.path.dirname(__file__))


def find_files_recursive(directory, file_type="json"):
    """
    通过文件类型查找文件
    :param directory:
    :param file_type:
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        file_list.extend([
            os.path.join(root, file)
            for file in files
            if file.endswith(f".{file_type}")
        ])
        for file_dir in dirs:
            file_list.extend(
                find_files_recursive(
                    os.path.join(
                        root,
                        file_dir),
                    file_type))
    return file_list


def write_to_file_with_suffix(filename, content):
    base_name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == "__main__":
    print(get_project_dir())
