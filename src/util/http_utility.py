#!/usr/bin/env python3
# coding: utf-8
# http_utility.py


import sys
import random
import json
import time
import socket
import http.client
import urllib.parse, urllib.request, urllib.error

from util.utility import merge_list_preserving_order
from util.codec import Codec


pc_browser_ua = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8",
        "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (iPad; CPU OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 OPR/39.0.2256.71",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
]

search_engine_ua = []


# 获取 URL 对应的 homepage
def get_homepage_url(url):
    if url is None or len(url) == 0:
        return
    components = urllib.parse.urlparse(url)
    l = list(components)
    for index in range(2, 6):
        l[index] = ''
    return urllib.parse.urlunparse(l)


# 处理掉 URL 中的特殊字符（eg. 空格、中文）
def format_url(url):
    if url is None or len(url) == 0:
        return
    components = urllib.parse.urlparse(url)
    l = list(components)
    for index in range(2, 6):
        l[index] = urllib.parse.quote(l[index], safe="/%=&,")
    return urllib.parse.urlunparse(l)


# 程序 sleep 一段时间
def sleep(interval):
    if isinstance(interval, int):
        time.sleep(interval)
    elif isinstance(interval, tuple) and len(interval) == 2:
        time.sleep(random.randint(*interval))


# 测试端口是否开放
def test_port_open(logger, ip, port, protocol='tcp', retry=2):
    this_func_name = sys._getframe().f_code.co_name
    retry = retry-1
    socket_type = socket.SOCK_STREAM
    if protocol == 'udp':
        socket_type = socket.SOCK_DGRAM
    elif protocol == 'raw':
        socket_type = socket.SOCK_RAW
    flag = False
    try:
        sock = socket.socket(socket.AF_INET, socket_type)
        sock.settimeout(5)
        sock.connect((ip, port))
        flag = True
    except OverflowError as e:
        logger.error("%s(): OverflowError" % this_func_name)
    except socket.timeout as e:
        logger.error("%s(): socket.timeout" % this_func_name)
        if retry > 0:
            return test_port_open(logger, ip, port, protocol, retry)
    except TimeoutError as e:
        logger.error("%s(): TimeoutError\terrno: %s\tstrerror: %s" % (this_func_name, e.errno, e.strerror))
        if retry > 0:
            return test_port_open(logger, ip, port, protocol, retry)
    except ConnectionRefusedError as e:
        logger.error("%s(): ConnectionRefusedError\terrno: %s\tstrerror: %s" % (this_func_name, e.errno, e.strerror))
        if retry > 0:
            return test_port_open(logger, ip, port, protocol, retry)
    except OSError as e:
        logger.error("%s(): OSError\terrno: %s\tstrerror: %s" % (this_func_name, e.errno, e.strerror))
        if retry > 0:
            return test_port_open(logger, ip, port, protocol, retry)
    finally:
        sock.close()
    logger.info("%s(): retry: %d\tip: %s\tport: %d\tprotocol: %s\tport open: %r" % (this_func_name, retry+1, ip, port, protocol, flag))
    return flag


# 解析得到 URL 对应的 HTML
# 返回值：成功，[delay, content]；失败，[-1, exception instance]
# 说明：之所以要返回异常类型，是因为有时侯外层调用者 caller 需要根据异常类型，做针对性地处理
def get_html_content(logger, url, post_data=None, referer=None, user_agent=None, proxy_pair=None, sleep_interval=3, retry=3):
    this_func_name = sys._getframe().f_code.co_name
    logger.info("%s(): retry\t\t%d" % (this_func_name, retry))
    retry = retry - 1
    start_timestamp = time.time()
    # 使用 HTTP/HTTPS 代理
    if proxy_pair is not None and len(proxy_pair) == 2:
        logger.debug("%s(): proxy_pair\t%s" % (this_func_name, json.dumps(proxy_pair, ensure_ascii=False)))
        proxy_dict = {}
        proxy_dict[proxy_pair[0]] = proxy_pair[1]
        proxy_handler = urllib.request.ProxyHandler(proxy_dict)
        opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPHandler, urllib.request.HTTPSHandler)
        urllib.request.install_opener(opener)
    # 伪造 HTTP request header
    _headers = {}
    post_data_binary = None
    if post_data is not None:
        logger.debug("%s(): post_data\t%s" % (this_func_name, json.dumps(post_data, ensure_ascii=False)))
        post_data_binary = urllib.parse.urlencode(post_data).encode('utf8')
    req = urllib.request.Request(url, data=post_data_binary, headers=_headers)
    if referer is not None and len(referer) != 0:
        logger.debug("%s(): Referer\t%s" % (this_func_name, referer))
        req.add_header('Referer', referer)
    if user_agent is not None and len(user_agent) != 0:
        logger.debug("%s(): User-Agent\t%s" % (this_func_name, user_agent))
        req.add_header('User-Agent', user_agent)
    try:
        logger.debug("%s(): before urlopen() ...\t%s" % (this_func_name, url))
        with urllib.request.urlopen(req, timeout=30) as response:
            logger.debug("%s(): after urlopen() ..." % this_func_name)
            if response.status != 200:
                logger.info("%s(): response.status\t%d" % (this_func_name, response.status))
            logger.debug("%s(): before HTTPResponse.read() ..." % this_func_name)
            content = response.read()
            # ms 级的时间差
            time_delta_in_ms = (time.time() - start_timestamp)*1000
            time_delta_in_ms = round(time_delta_in_ms, 1)
            logger.debug("%s(): after HTTPResponse.read() ..." % this_func_name)
            encodings = Codec.encoding_list
            encoding = response.headers.get_content_charset()
            logger.info("%s(): encoding\t%s" % (this_func_name, encoding))
            if encoding is not None:
                encodings = merge_list_preserving_order([Codec.encoding_map.get(encoding, encoding)], Codec.encoding_list)
            logger.info("%s(): encodings\t%s" % (this_func_name, encodings))
            html_content = None
            for encoding in encodings:
                html_content = Codec.decode(logger, content, encoding)
                if html_content is not None:
                    break
            # 最终返回值有可能为：[time_delta_in_ms, None]
            return time_delta_in_ms, html_content
    except urllib.error.HTTPError as e:
        logger.error("%s(): urllib.error.HTTPError\t%s\t%s\t%s\t%s" % (this_func_name, url, e.getcode(), e.errno, e.reason))
        # if e.getcode() == 403 or e.getcode() == 404 or e.getcode() == 502:
        return -1, e
    except urllib.error.URLError as e:
        logger.error("%s(): urllib.error.URLError\t%s\t%s\t%s" % (this_func_name, url, e.errno, e.reason))
        return -1, e
    except socket.timeout as e:
        logger.error("%s(): socket.timeout\t%s" % (this_func_name, url))
        if retry > 0:
            return get_html_content(logger, url, post_data, referer, user_agent, proxy_pair, sleep_interval, retry)
        return -1, e
    except ConnectionResetError as e:
        logger.error("%s(): ConnectionResetError" % this_func_name)
        if retry > 0:
            sleep(sleep_interval)
            return get_html_content(logger, url, post_data, referer, user_agent, proxy_pair, sleep_interval, retry)
        return -1, e
    except http.client.InvalidURL as e:
        logger.error("%s(): http.client.InvalidURL\t%s" % (this_func_name, url))
        return -1, e
    except http.client.BadStatusLine as e:
        logger.error("%s(): http.client.BadStatusLine" % this_func_name)
        if retry > 0:
            sleep(sleep_interval)
            return get_html_content(logger, url, post_data, referer, user_agent, proxy_pair, sleep_interval, retry)
        return -1, e
    # URL 中含有特殊字符（eg. 空格、中文）
    except UnicodeEncodeError as e:
        logger.error("%s(): UnicodeEncodeError\t%s\t%s\t%s" % (this_func_name, url, e.encoding, e.reason))
        formatted_url = format_url(url)
        logger.error("%s(): formatted URL\t\t%s" % (this_func_name, formatted_url))
        if retry > 0:
            return get_html_content(logger, url, post_data, referer, user_agent, proxy_pair, sleep_interval, retry)
        return -1, e
    except TypeError as e:
        logger.error("%s(): TypeError\t%s" % (this_func_name, url))
        return -1, e
    # 由 http.client.HTTPResponse 的 read() 方法产生
    except http.client.IncompleteRead as e:
        logger.error("%s(): http.client.IncompleteRead\t%s" % (this_func_name, url))
        if retry > 0:
            return get_html_content(logger, url, post_data, referer, user_agent, proxy_pair, sleep_interval, retry)
        return -1, e


if __name__ == '__main__':
    result = random.choice(pc_browser_ua)
    print(result)

    result = get_homepage_url("https://www.zhihu.com/question/19861840")
    print(result)




