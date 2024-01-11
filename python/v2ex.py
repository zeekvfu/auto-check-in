#!/usr/bin/env python3
# coding: utf-8
# v2ex.py


import os, sys, glob, time, random, json

from pathlib import Path
from lxml    import etree
from io      import StringIO

from util      import get_logger, to_minified_json
from http_util import curl
from file_op   import FileOp


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


# cookie 参数：A2。
def v2ex_check_in(logger, file):
    this_func_name = sys._getframe().f_code.co_name

    user_name = Path(file).stem
    parser    = etree.HTMLParser()

    url = 'https://v2ex.com/mission/daily'
    rsp = curl(url, cookie_file=file)
    if "每日登录奖励已领取" in rsp:
        logger.debug("%s(): user_name:%s url:%s coin already collected..." % (this_func_name, user_name, url))
        return

    tree         = etree.parse(StringIO(rsp), parser)
    s            = tree.xpath('//input[@type="button" and @class="super normal button" and @value="领取 X 铜币" and contains(@onclick, "location.href")]/@onclick')[0]
    path         = s[s.index("'")+1: s.rindex("'")]
    homepage_url = 'https://v2ex.com'
    url          = "%s%s" % (homepage_url, path)
    rsp          = curl(url, ua_type='pc', cookie_file=file)
    if "已成功领取每日登录奖励" in rsp:
        logger.debug("%s(): user_name:%s url:%s coin successfully collected!" % (this_func_name, user_name, url))
    else:
        logger.debug("%s(): user_name:%s url:%s collect coin failed!" % (this_func_name, user_name, url))

    return


def main():
    this_func_name = sys._getframe().f_code.co_name

    script_dir = get_script_dir()
    config     = FileOp.load_json_config('%s/../conf/check_in.json' % script_dir)
    logger     = get_logger('%s/../log/v2ex.log' % script_dir, config['log_level'])

    logger.debug('[%s] ****************************************************************************************************' % this_func_name)

    if 'apps' in config and 'v2ex' in config['apps'] and 'cookie_file_dir' in config['apps']['v2ex']:
        files = glob.glob("%s/*.txt" % config['apps']['v2ex']['cookie_file_dir'])
        for file in files:
            v2ex_check_in(logger, file)
            time.sleep(random.randint(0, 60))


if __name__ == '__main__':
    main()


