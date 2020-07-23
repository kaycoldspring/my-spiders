# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
from twisted.internet.error import TCPTimedOutError, ConnectionRefusedError
from urllib import parse
from util.proxies import check_proxies


class MyMiddleware(object):

    def process_exception(self, request, exception, spider):
        """异常处理"""
        if isinstance(exception, (TCPTimedOutError, ConnectionRefusedError)):
            # 将会被重新放入 SCHEDULER 中并在以后重新进行下载, 这会停止后续中间件的 process_exception
            spider.logger.error("Exception URL: %s" % request.url)
            request.meta['proxy'] = None
            return request.replace(url=request.url, dont_filter=True)

        # 为了效率问题,直接将出错的问题下的公司名字放到出错的set中,以后再处理
        # company = request.meta["company_name"]
        # spider.server.sadd(spider.fail_queue, company)
        # return None

    def process_request(self, request, spider):
        """设置代理"""
        if spider.event_flg % 2 == 0:
            # 偶数线程, 此时进行封锁
            spider.event.wait()
            proxies_value = spider.proxies.get_proxies()
        else:
            # 奇数线程, 此时释放锁
            proxies_value = spider.proxies.get_proxies()
            if not check_proxies(**proxies_value):
                # 在更新代理之前加锁
                if proxies_value == spider.proxies_value:
                    # 说明代理失效
                    proxies_value = spider.proxies.get_proxies(update=True)
                    spider.proxies_value = proxies_value
                else:
                    # 说明是单线程的代理没有更换
                    proxies_value = spider.proxies_value
            spider.event.set()
        spider.event_flg += 1
        spider.event_flg = 1 if spider.event_flg >= 16 else spider.event_flg
        proxies_value = "http://{ip}:{port}".format(**proxies_value)
        # spider.logger.info("The current proxies_value is %s" % proxies_value)
        request.meta['proxy'] = proxies_value

    def process_response(self, request, response, spider):
        # 检测响应结果,出现302说明这个ip被封了,删除更新ip即可
        if response.status == 302 or "check" in response.url:
            company = request.meta["company_name"]
            spider.server.sadd(spider.fail_queue, company)
            # # 302 的 url 需要重新抽取更换
            from_url = spider.pattern_302.match(response.url).group(1)
            from_url = parse.unquote(from_url)
            # # 因为这个还是会发送到 process_request 中取请求,所以直接在那里会进行更新
            request.meta['proxy'] = None
            return request.replace(url=from_url, dont_filter=True)
        return response


class ScrapyRequestSpiderMiddleware(object):
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
