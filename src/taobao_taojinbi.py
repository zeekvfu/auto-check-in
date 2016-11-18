#!/usr/bin/env python3
# coding: utf-8
# taobao_taojinbi.py


import os
import sys
import time

from io import StringIO
from lxml import etree

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from util.utility import get_logger
from util.http_utility import pc_browser_ua
from util.file_utility import FileUtility


class TaoBao:

    homepage_url = 'https://www.taobao.com/'
    # 宝贝收藏
    item_collect_list_url = 'https://shoucang.taobao.com/item_collect_n.htm'
    # 店铺收藏
    shop_collect_list_url = 'https://shoucang.taobao.com/shop_collect_list_n.htm'

    login_url = 'https://login.taobao.com/'
    regular_check_in_url = 'https://taojinbi.taobao.com/index.htm'
    shop_check_in_url = 'https://www.taobao.com/markets/taojinbi/happy-valley'
    luck4ever_taojinbi_url = 'http://www.luck4ever.net/archives/taojinbi-50.html'


    def __init__(self, logger, user_name, password):
        this_func_name = sys._getframe().f_code.co_name
        self.logger = logger
        self.logger.debug("%s(): start ..." % this_func_name)
        self.user_name = user_name
        self.password = password
        # Chrome
        self.driver = Chrome()
        # Firefox
        # ff_binary = FirefoxBinary(firefox_path='/usr/bin/firefox-bin', log_file='/tmp/firefox-bin.log')
        # ff_capabilities = DesiredCapabilities.FIREFOX
        # ff_capabilities['marionette'] = True
        # self.driver = Firefox(firefox_binary=ff_binary, capabilities=ff_capabilities, log_path='/tmp/geckodriver.log')

        self.driver.implicitly_wait(15)


    def login(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.login_url)
        # 登录方式切换：二维码扫描、用户名密码
        try:
            self.driver.find_element_by_xpath('//div[@class="login-switch" and @onselectstart="return false;"]/i[@id="J_Quick2Static" and @class="iconfont static"]').click()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)

        self.driver.find_element_by_id("TPL_username_1").clear()
        self.driver.find_element_by_id("TPL_username_1").send_keys(self.user_name)
        self.driver.find_element_by_id("TPL_password_1").clear()
        self.driver.find_element_by_id("TPL_password_1").send_keys(self.password)
        self.driver.find_element_by_id("J_SubmitStatic").click()

        # 请按住滑块，拖动到最右边
        try:
            source = self.driver.find_element_by_xpath('//span[@id="nc_1_n1z" and @class="nc_iconfont btn_slide" and @style]')
            ActionChains(self.driver).drag_and_drop_by_offset(source, 1200, 0).perform()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)
        return


    # 普通签到
    def regular_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.regular_check_in_url)
        time.sleep(5)
        try:
            self.driver.find_element_by_xpath('//div[@class="my-btns"]/a[@class="btn login-btn J_GoTodayBtn" and @href="#" and contains(text(), "今日可领")]').click()
            time.sleep(5)
            source = self.driver.find_element_by_xpath('//span[@class="nc-lang-cnt" and @data-nc-lang="_startTEXT" and text()="请按住滑块，拖动到最右边"]')
            ActionChains(self.driver).drag_and_drop_by_offset(source, 1200, 0).perform()
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)
        return


    # 获取「店铺签到」的 URL 列表
    def parse_shop_url_list(self, content):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        urls = tree.xpath('//div[@class="content"]/div[@class="item"]/a[@class="item-link"]/@href')
        urls = [ 'https:' + url for url in  urls ]
        self.logger.debug("%s(): urls\t%s" % (this_func_name, urls))
        return urls


    # 店铺签到
    def shop_check_in(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.shop_check_in_url)
        time.sleep(5)
        urls = self.parse_shop_url_list(self.driver.page_source)
        for url in urls:
            self.driver.get(url)
            time.sleep(5)

            self.driver.find_element_by_xpath('//a[@href="#" and @class="now-take J_NowSignIn" and text()="立即签到"]').click()

            # element = self.driver.find_element_by_xpath('//a[@href="#" and @class="now-take J_NowSignIn" and text()="立即签到"]')
            # ActionChains(self.driver).click(element).perform()

            # element = self.driver.find_element_by_xpath('//a[@href="#" and @class="now-take J_NowSignIn" and text()="立即签到"]')
            # ActionChains(self.driver).move_by_offset(-100, -100).context_click(element).perform()
            # time.sleep(5)
            # element.send_keys(Keys.ESCAPE);
            # element.send_keys(Keys.ENTER);


    # 收藏店铺
    def favorite_shop(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): current_url: %s" % (this_func_name, self.driver.current_url))
        self.driver.find_element_by_xpath('//p[@class="btns"]/button[@type="submit" and @class="bt-submit"]').click()
        # 领取的淘金币可能超过每日上限
        flag = True
        if '您今天获得的淘金币将达上限，本次领取失败' in self.driver.page_source:
            flag = False
        self.logger.debug("%s(): current_url: %s\t\tflag:%s" % (this_func_name, self.driver.current_url, flag))
        return flag


    # 分享店铺
    def share_shop(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): current_url: %s" % (this_func_name, self.driver.current_url))
        if '该店铺不存在,无法进行分享' in self.driver.page_source:
            self.logger.debug("%s(): current_url: %s\t\tflag:%s" % (this_func_name, self.driver.current_url, True))
            return True
        flag = True
        try:
            self.driver.find_element_by_xpath('//div[@class="operate"]/a[@class="continue J_Continue J_Submit" and @href="#" and text()="立即分享"]').click()
            time.sleep(2)
            # 弹出警告框，无法再分享
            # 一直蒙头分享啊?歇歇,去我的淘宝里看看朋友在分享些啥吧
            if self.driver.find_element_by_xpath('//div[@class="sns-widget-alert-buttons clearfix"]/a[@class="sns-widget-alert-sure" and @title="确定" and text()="确 定"]').is_displayed():
                flag = False
        except NoSuchElementException as e:
            self.logger.debug("%s(): NoSuchElementException" % this_func_name)
        finally:
            self.logger.debug("%s(): current_url: %s\t\tflag:%s" % (this_func_name, self.driver.current_url, flag))
            return flag


    # 在 luck4ever.net 上领取淘金币
    def luck4ever_taojinbi(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.driver.get(self.luck4ever_taojinbi_url)

        # 喜欢宝贝/收藏店铺
        elements = self.driver.find_elements_by_xpath('//p[@style="white-space: normal;" and contains(text(), "喜欢宝贝/")]/a[@target="_blank" and contains(@href, "https://favorite.taobao.com/popup/") and @rel="nofollow" and position()<3]')
        for element in elements:
            element.click()
            # 等待新的 tab 被加载
            time.sleep(5)
            # 切换到新的 window 下
            self.driver.switch_to.window(self.driver.window_handles[1])
            flag = self.favorite_shop()
            # 关闭当前 window
            self.driver.close()
            # 切换回原来的 window
            self.driver.switch_to.window(self.driver.window_handles[0])
            if not flag:
                break

        # 分享店铺
        elements = self.driver.find_elements_by_xpath('//p[@style="white-space: normal;" and contains(text(), "分享店铺:")]/a[@target="_blank" and contains(@href, "https://share.jianghu.taobao.com/share/") and @rel="nofollow"]')
        for element in elements:
            element.click()
            # 等待新的 tab 被加载
            time.sleep(5)
            # 切换到新的 window 下
            self.driver.switch_to.window(self.driver.window_handles[1])
            flag = self.share_shop()
            # 关闭当前 window
            self.driver.close()
            # 切换回原来的 window
            self.driver.switch_to.window(self.driver.window_handles[0])
            if not flag:
                break

        return


    def run(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): start ..." % this_func_name)
        self.login()
        self.regular_check_in()
        self.shop_check_in()
        self.luck4ever_taojinbi()
        self.driver.quit()
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




