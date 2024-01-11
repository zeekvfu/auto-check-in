#!/usr/bin/env python3
# coding: utf-8
# rq.py


"""
TODO:
数据库增加字段：insert_time、begin_time、months
签到失败通知。
"""


import os, sys, time, random, json

from util      import get_logger, to_minified_json
from http_util import curl
from file_op   import FileOp


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def rq_check_in(logger, cookies):
    this_func_name = sys._getframe().f_code.co_name

    url_prefix = "https://rq.runningquotient.cn/MiniApi/SignIn/get_sign_day_list/rand/"
    url_prefix = "https://rq.runningquotient.cn/MiniApi/SignIn/sign_in/rand/"
    for key, value in cookies.items():
        for x in value:
            rand_int             = random.randint(16, 17)
            rand_float           = random.random()
            rand_float_formatted = ("{:.%df}" % rand_int).format(rand_float)
            url                  = "%s%s" % (url_prefix, rand_float_formatted)
            cookie_str           = "%s=%s" % (key, x)
            rsp                  = curl(url, ua_type='iphone', cookie=cookie_str)
            rsp_formatted        = to_minified_json(json.loads(rsp))
            logger.debug("[%s] url:%s cookie_str:%s rsp_formatted:%s" % (this_func_name, url, cookie_str, rsp_formatted))
            time.sleep(random.randint(0, 60))


def main():
    this_func_name = sys._getframe().f_code.co_name

    script_dir = get_script_dir()
    config     = FileOp.load_json_config('%s/../conf/check_in.json' % script_dir)
    logger     = get_logger('%s/../log/rq.log' % script_dir, config['log_level'])

    logger.debug('[%s] ****************************************************************************************************' % this_func_name)

    if 'apps' in config and 'rq' in config['apps']:
        rq_check_in(logger, config['apps']['rq'])


if __name__ == '__main__':
    main()


