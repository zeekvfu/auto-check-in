#!/usr/bin/env python3
# coding: utf-8
# v2ex_copper_coin.py


import os
import sys
import random
import time
import requests

from io import StringIO
from lxml import etree

from util.utility import get_logger
from util.http_utility import pc_browser_ua
from util.file_utility import FileUtility


class V2EX:

    homepage_url = 'https://www.v2ex.com'
    login_url = 'https://www.v2ex.com/signin'
    check_in_url = 'https://www.v2ex.com/mission/daily'


    def __init__(self, logger, user_name, password):
        this_func_name = sys._getframe().f_code.co_name

        self.logger = logger
        self.user_name = user_name
        self.password = password

        session = requests.Session()
        session.headers = {
                'User-Agent': random.choice(pc_browser_ua)
                }
        self.session = session

        self.logger.debug("%s(): user_name: %s\tpassword: %s" % (this_func_name, user_name, password))
        self.logger.debug("%s(): start ..." % this_func_name)


    def get_login_parameters(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        response = self.session.get(self.login_url)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        elements = tree.xpath('//form[@method="post" and @action="/signin"]/table[@cellpadding="5" and @cellspacing="0" and @border="0" and @width="100%"]//tr[position()<last()]/td[2]/input')
        user_name_key = elements[0].xpath('@name')[0]
        password_key = elements[1].xpath('@name')[0]
        once = elements[2].xpath('@value')[0]
        self.logger.debug("%s(): user_name_key: %s\tpassword_key: %s\tonce: %s" % (this_func_name, user_name_key, password_key, once))
        return user_name_key, password_key, once


    def login(self, user_name_key, password_key, once):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        # 必须带上 referer
        self.session.headers.update({'referer': self.login_url})
        d = {
                user_name_key: self.user_name,
                password_key: self.password,
                'once': once,
                'next': '/'
                }
        response = self.session.post(self.login_url, d)
        flag = False
        if "条未读提醒" in response.text:
            flag = True
        self.logger.debug("%s(): url: %s\tPOST: %s\tlogin: %s" % (this_func_name, self.login_url, d, flag))
        return flag


    # 领取铜币
    def get_copper_coin(self, once):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)

        # 重新获取 once 的值
        response = self.session.get(self.check_in_url)
        if "每日登录奖励已领取" in response.text:
            self.logger.debug("%s(): copper coin already fetched ..." % this_func_name)
            return
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        s = tree.xpath('//input[@type="button" and @class="super normal button" and @value="领取 X 铜币" and contains(@onclick, "location.href")]/@onclick')[0]
        path = s[s.index("'")+1: s.rindex("'")]

        # 领取铜币
        url = self.homepage_url + path
        response = self.session.get(url)
        flag = False
        if "已成功领取每日登录奖励" in response.text:
            flag = True
        self.logger.debug("%s(): url: %s\tcopper_coin: %s" % (this_func_name, url, flag))
        return


    def run(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        user_name_key, password_key, once = self.get_login_parameters()
        if self.login(user_name_key, password_key, once):
            self.get_copper_coin(once)
        return


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    this_func_name = __name__

    script_dir = get_script_dir()
    config = FileUtility.load_json_config('%s/../conf/check_in.config.json' % script_dir)
    timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
    logger = get_logger("%s/../log/v2ex.%s.log" % (script_dir, timestamp), config['log_level'])
    logger.debug("%s(): ****************************************************************************************************" % this_func_name)

    for item in config['v2ex']:
        v2ex = V2EX(logger, item['user_name'], item['password'])
        v2ex.run()


