# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from urllib import parse
import requests
from fake_useragent import UserAgent
from scrapy import signals
from SXR.db import REDISCLIENT
from scrapy import signals


class SxrSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SxrDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = REDISCLIENT()

    def get_random_proxy(self):
        """
        连接数据库获取随机的proxy
        :return: proxy
        """
        try:
            proxy = self.db.random()
            self.db.check()
            return proxy
        except requests.ConnectionError:
            # 出现连接错误
            return False

    def process_request(self, request, spider):
        """
        每个请求都会经过这里，在此添加代理IP
        :param request:
        :param spider:
        :return:
        """
        if request.meta.get('retry_times'):
            print("进入代理IP中间件中===================================")
            # 在当前代理不能使用时才选择更换
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理' + proxy)
                request.meta['proxy'] = uri

    # def process_response(self, request, response, spider):
    #     """
    #     如果响应中出现重定向则需要重新更换proxy
    #     :param request:
    #     :param response:
    #     :param spider:
    #     :return:
    #     """
    #     if response.status == 302 or 301:
    #         print("进入重定向？？？？？？？？？？？？？？？？？？？？？？？")
    #         time.sleep(5)
    #         # 如果出现重定向，获取重定向的地址
    #         redirect_url = response.url
    #         if 'login' in redirect_url:
    #             # 重定向到登陆界面，cookies失效
    #             self.logger.info('cookies 失效')
    #             # 如果出现重定向说明请求失败，获取一个重回新请求
    #             proxy = self.get_random_proxy()
    #             # 返回当前的请求重新加入爬取队列
    #             if proxy:
    #                 uri = 'https://{proxy}'.format(proxy=proxy)
    #                 self.logger.debug('使用代理' + proxy)
    #                 request.meta['proxy'] = uri
    #                 return request
    #     return response

class Uamid(object):
    # 初始化 注意一定要user_agent，不然容易报错
    def __init__(self, crawler):
        super(Uamid, self).__init__()
        self.ua = UserAgent()
        # 从settings.py中读取RANDOM_UA_TYPE配置，如果没有则采用默认的random，达到可配置的目的
        # 默认是random随机选择。但是可以在配置指定ie或者Firefox等浏览器的不同版本
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 请求处理
    def process_request(self, request, spider):
        # 先随机选择一个用户代理
        def get_ua_type():
            '''
            闭包函数
            读取上面的ua_type设置，让process_request直接调用本get_ua
            :return:
            '''
            print("已经获得用户代理，开始爬取")
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent',get_ua_type())