#!/usr/bin/env python3
# coding: utf-8
# file_utility.py


import json
from collections import OrderedDict


class FileUtility():

    # 按行读取文件，包括空行
    @staticmethod
    def read_file_by_line(file_name):
        lines = []
        with open(file_name, encoding='utf-8', mode='r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                lines.append(line.rstrip('[\r\n]'))
        return lines


    # 按行读取文件（行去重）
    @staticmethod
    def read_unique_lines(file_name):
        unique_lines = []
        with open(file_name, encoding='utf-8', mode='r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.rstrip('[\r\n]')
                if line in unique_lines:
                    continue
                unique_lines.append(line)
        return unique_lines


    # 读取配置文件
    @staticmethod
    def read_config(file_name):
        with open(file_name, encoding='utf-8', mode='r') as f:
            content = f.read()
            return eval(content)


    # 读取 JSON 配置文件
    @staticmethod
    def load_json_config(file_name, keep_order=False):
        with open(file_name, encoding='utf-8', mode='r') as f:
            content = f.read()
            if keep_order:
                # 保持 JSON 文件里 dict 原来的顺序
                return json.loads(content, object_pairs_hook=OrderedDict)
            return json.loads(content)


    # 读取 Python data structure 形式的配置文件
    @staticmethod
    def eval_config(file_name, keep_order=False):
        with open(file_name, encoding='utf-8', mode='r') as f:
            content = f.read()
            return eval(content)


    # 将字符串 s 写入文件
    @staticmethod
    def write_to_file(file_name, s, open_mode='w'):
        with open(file_name, encoding='utf-8', mode=open_mode) as f:
            f.write(s)




