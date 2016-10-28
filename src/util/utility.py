#!/usr/bin/env python3
# coding: utf-8
# utility.py


import os
import json
import random
import logging
import itertools
import datetime
import re

from collections import defaultdict, OrderedDict


# 获取脚本所在的路径
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


# 从 sequence 中随机获取一个元素
# use `random.choice()` instead
def random_elem(l):
    if l is None or len(l) == 0:
        return
    index = random.randint(0, len(l)-1)
    return l[index]


def empty_str_to_none(s):
    if s is not None and s == '':
        s = None
    return s


# 与 str() 方法的区别是，可以自定义将 None 转化成什么 str
def obj_to_str(obj, none_to_what='', datetime_format='%Y-%m-%d %H:%M:%S'):
    result = None
    if obj is None:
        result = none_to_what
    elif isinstance(obj, datetime.datetime):
        result = obj.strftime(datetime_format)
    else:
        result = str(obj)
    return result


def obj_to_db_field(obj):
    result = None
    if obj is None:
        result = 'null'
    elif isinstance(obj, str):
        result = "'%s'" % obj
    elif isinstance(obj, (bool, int, float)):
        result = str(obj)
    elif isinstance(obj, datetime.datetime):
        s = obj_to_str(obj)
        result = obj_to_db_field(s)
    return result


def obj_to_datetime(obj, datetime_format='%Y-%m-%d %H:%M:%S'):
    result = None
    if isinstance(obj, datetime.datetime):
        result = obj
    elif isinstance(obj, str):
        result = datetime.datetime.strptime(obj, datetime_format)
    return result


# faltten a list
def flatten_list(l):
    return [ item for sublist in l for item in sublist ]


# 将 list 合并起来，并且保持相对顺序（list 间相对顺序 + list 内元素相对顺序）
def merge_list_preserving_order(*args):
    result = itertools.chain(*args)
    return list(OrderedDict.fromkeys(result))


# 合并 dict
def merge_dict(*dict_args):
    return merge_dict_in_sequence(dict_args)


def merge_dict_in_sequence(l):
    dd = defaultdict(list)
    for d in l:
        for key, value in d.items():
            dd[key].append(value)
    return dd


# 去掉 list 中的空白行
def trim_blank_lines_in_list(lines):
    result = []
    for line in lines:
        l = line.strip()
        if l:        # 字符串非空
            result.append(l)
    return result


def get_logger(log_file, log_level=logging.DEBUG):
    _format = '%(asctime)s %(process)d %(thread)d %(levelname)s | %(message)s'
    formatter = logging.Formatter(_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(log_file)
    logger.addHandler(file_handler)
    if isinstance(log_level, str):
        log_level = eval(log_level)
    logger.setLevel(log_level)
    return logger


if __name__ == '__main__':
    print(__file__)
    print(os.path.realpath(__file__))
    print(get_script_dir())




