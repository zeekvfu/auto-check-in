#!/usr/bin/env python3
# coding: utf-8
# taobao_taojinbi.py


import os
import sys
import time

from selenium import webdriver

from util.utility import get_logger
from util.http_utility import pc_browser_ua
from util.file_utility import FileUtility


class TaoBao:

    homepage_url = 'https://www.taobao.com/'
    login_url = 'https://login.taobao.com/'
    regular_check_in_url = 'https://taojinbi.taobao.com/index.htm'
    store_check_in_url = 'https://www.taobao.com/markets/taojinbi/happy-valley'


    def __init__(self, logger, user_name, password):
        this_func_name = sys._getframe().f_code.co_name

        self.logger = logger
        self.user_name = user_name
        self.password = password
        self.driver = webdriver.Chrome()


    def login(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.login_url)
        self.driver.find_element_by_id("TPL_username_1").send_keys(self.user_name)
        self.driver.find_element_by_id("TPL_password_1").send_keys(self.password)
        self.driver.find_element_by_id("J_SubmitStatic").click()
        self.driver.implicitly_wait(5)


    # 普通签到
    def regular_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.regular_check_in_url)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//a[@class="btn login-btn J_GoTodayBtn" and @href="#" and @data-spm-anchor-id]').click()
        self.driver.find_element_by_xpath('//span[@class="nc-lang-cnt" and @data-nc-lang="_startTEXT" and text()="请按住滑块，拖动到最右边"]').click()


    # 店铺签到
    def store_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.store_check_in_url)
        self.driver.implicitly_wait(5)
        elements = self.driver.find_elements_by_xpath('//div[@class="content"]/div[@class="item"]')
        for element in elements:
            element.click()
            self.driver.find_element_by_xpath('//a[@href="#" and @class="now-take J_NowSignIn" and text()="立即签到"]').click()


    def run(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.login()
        self.regular_check_in()
        self.store_check_in()
        return


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    this_func_name = __name__

    script_dir = get_script_dir()
    config = FileUtility.load_json_config('%s/../conf/check_in.config.json' % script_dir)
    timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
    logger = get_logger("%s/../log/taobao.%s.log" % (script_dir, timestamp), config['log_level'])
    logger.debug("%s(): ****************************************************************************************************" % this_func_name)

    for item in config['taobao']:
        taobao = TaoBao(logger, item['user_name'], item['password'])
        taobao.run()




