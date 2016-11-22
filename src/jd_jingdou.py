#!/usr/bin/env python3
# coding: utf-8
# jd_jingdou.py


import os
import sys
import time

from selenium.webdriver import PhantomJS, Chrome, Firefox
from selenium.common.exceptions import NoSuchElementException

from util.utility import get_logger
from util.http_utility import pc_browser_ua
from util.file_utility import FileUtility


class JD:

    homepage_url = 'https://www.jd.com/'
    login_url = 'https://passport.jd.com/new/login.aspx'
    # 京东会员
    vip_url = 'http://vip.jd.com/'
    # 京东金融
    finance_url = 'http://vip.jr.jd.com/'


    def __init__(self, logger, user_name, password):
        this_func_name = sys._getframe().f_code.co_name
        self.logger = logger
        self.logger.debug("%s(): start ..." % this_func_name)
        self.user_name = user_name
        self.password = password
        # Chrome
        self.driver = Chrome()
        self.driver.implicitly_wait(15)


    def login(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.login_url)
        # 登录方式切换：扫码登录、账户登录
        try:
            self.driver.find_element_by_xpath('//div[@class="login-tab login-tab-r"]/a[@href="javascript:void(0)" and contains(@clstag, "pageclick|keycount|") and @class and contains(@style, "outline: rgb(")]').click()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)

        # 用户名
        element = self.driver.find_element_by_xpath('//div[@class="item item-fore1"]/input[@id="loginname" and @type="text" and @class="itxt" and @name="loginname" and @tabindex="1" and @autocomplete="off" and @placeholder="邮箱/用户名/已验证手机"]')
        element.clear()
        element.send_keys(self.user_name)
        # 密码
        element = self.driver.find_element_by_xpath('//div[@id="entry" and @class="item item-fore2" and @style="visibility: visible;"]/input[@type="password" and @id="nloginpwd" and @name="nloginpwd" and @class="itxt itxt-error" and @tabindex="2" and @autocomplete="off" and @placeholder="密码"]')
        element.clear()
        element.send_keys(self.password)
        # 自动登录
        element = self.driver.find_element_by_xpath('//div[@class="item item-fore3"]/div[@class="safe"]/span/input[@id="autoLogin" and @name="chkRememberMe" and @type="checkbox" and @class="jdcheckbox" and @tabindex="3" and contains(@clstag, "pageclick|keycount|")]')
        element.click()
        # 点击登录
        self.driver.find_element_by_xpath('//div[@class="item item-fore5"]/div[@class="login-btn"]/a[@href="javascript:;" and @class="btn-img btn-entry" and @id="loginsubmit" and @tabindex="6"]').click()
        time.sleep(3)

        flag = False
        if self.driver.find_element_by_xpath('//div[@class="user_info_show"]/p/a[@href="//home.jd.com"]').is_displayed():
            flag = True
        self.logger.debug("%s(): login: %s" % (this_func_name, flag))
        return flag


    # 京东会员，签到领京豆
    def vip_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.vip_url)
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//a[@href="javascript:void(0)" and @clstag="vip|keycount|homepage|checkin" and @id="checkinBtn" and @class="item checkin    checkin-ready  "]/i[@class="icon-set"]').click()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)
        time.sleep(3)
        return


    # 京东金融，签到领京豆
    def finance_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.finance_url)
        time.sleep(3)
        try:
            # self.driver.find_element_by_xpath('//div[@class="qian-icon x-qian"]/div[@class="x-yi-q"]').click()
            self.driver.find_element_by_xpath('//div[@class="qian-icon x-qian"]').click()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)
        time.sleep(3)
        return


    def run(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        if self.login():
            self.vip_check_in()
            self.finance_check_in()
        self.driver.quit()
        return


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    this_func_name = __name__

    script_dir = get_script_dir()
    config = FileUtility.load_json_config('%s/../conf/check_in.config.json' % script_dir)
    timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
    logger = get_logger("%s/../log/jd.%s.log" % (script_dir, timestamp), config['log_level'])
    logger.debug("%s(): ****************************************************************************************************" % this_func_name)

    for item in config['jd']:
        jd = JD(logger, item['user_name'], item['password'])
        jd.run()




