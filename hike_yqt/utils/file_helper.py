# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:35
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : file_helper.py

import os


def is_exist_directory(path):
    return os.path.exists(path)


def get_directory_name(file_path):
    return


def create_directorys_by_file_path(file_path):
    os.makedirs(os.path.dirname(file_path))


if __name__ == '__main__':
    print(os.makedirs('./data/data1/data2/', exist_ok=True))
    print(is_exist_directory("./log"))
