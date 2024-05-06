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


# cookie 参数 A2，有效期约 90 天。
def v2ex_check_in(logger, file):
    this_func_name = sys._getframe().f_code.co_name

    user_name = Path(file).stem
    ua_type   = 'mac_chrome'
    parser    = etree.HTMLParser()

    url_old = 'https://v2ex.com/mission/daily'
    url     = url_old
    rsp     = curl(url, ua_type=ua_type, cookie_file=file)
    if "每日登录奖励已领取" in rsp:
        logger.debug("%s(): user_name:%s url:%s coin already collected..." % (this_func_name, user_name, url))
        return
    time.sleep(random.randint(1, 5))

    tree         = etree.parse(StringIO(rsp), parser)
    s            = tree.xpath('//input[@type="button" and @class="super normal button" and @value="领取 X 铜币" and contains(@onclick, "location.href")]/@onclick')[0]
    path         = s[s.index("'")+1: s.rindex("'")]
    homepage_url = 'https://v2ex.com'
    url          = "%s%s" % (homepage_url, path)
    rsp          = curl(url, ua_type=ua_type, cookie_file=file, referer=url_old, req_headers=['Content-Type: text/html; charset=UTF-8'])
    # logger.debug("%s(): user_name:%s url:%s rsp:%s" % (this_func_name, user_name, url, rsp))

    msg = None
    if "已成功领取每日登录奖励" in rsp:
        msg = "coin successfully collected!"
    # 可能被要求重新点击领取
    elif "请重新点击一次以领取每日登录奖励" in rsp:
        msg = "requested to click again!"
    else:
        msg = "collect coin failed!"
    logger.debug("%s(): user_name:%s url:%s %s" % (this_func_name, user_name, url, msg))

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
            time.sleep(random.randint(300, 600))


if __name__ == '__main__':
    main()


