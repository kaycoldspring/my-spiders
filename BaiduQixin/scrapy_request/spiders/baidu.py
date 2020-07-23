# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
import json
from scrapy_redis.spiders import RedisSpider
import re
import time
import execjs
from scrapy_request.items import XinbdItem
from util.proxies import Proxies
from util.db import get_redis_cli
from scrapy.spidermiddlewares.httperror import HttpError
from threading import Event
# twisted 异常捕获
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError


"""
	1. 请求第一个页面数据, 获取到列表页面中的详情页 url
	2. 请求详情页面 url, 从详情页抽取出关键字段执行js获取到工商数据的url
	3. 请求上述 url, 获取到数据入库
"""

default_value = 'null'


class BAIDU_SPIDER(RedisSpider):
	name = 'baidu_spider'
	custom_settings = dict(
		SCHEDULER="scrapy_redis.scheduler.Scheduler",
		DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter",
		# SCHEDULER_PERSIST=True,
		# CONCURRENT_REQUESTS=32, 			# 增加全局并发设置
		REACTOR_THREADPOOL_MAXSIZE=16, 		# 增加 Twisted IO 线程池的最大值
		LOG_LEVEL='DEBUG',
		COOKIES_ENABLED=False,			# 禁用 cookie
		# REDIRECT_ENABLED=False,		# 禁用重定向
		REDIS_HOST='127.0.0.1',
		REDIS_PORT='6379',
		REDIS_PARAMS={
			# 'password': ''
			'db':       2
		},
		DOWNLOADER_MIDDLEWARES={
			'scrapy_request.middlewares.MyMiddleware': 100,
		},
		SPIDER_MIDDLEWARES={
			'scrapy_request.middlewares.ScrapyRequestSpiderMiddleware': 543,
		},
		RETRY_ENABLED=False,  			# 重试中间件 指定关闭 默认为 True 是开启状态
		# RETRY_HTTP_CODES=[302], 		# 指定要重试的 HTTP 状态码，其它错误会被丢弃
		# RETRY_TIMES=2,			    # 指定重试次数
		AUTOTHROTTLE_ENABLED=True,    # 自动限速扩展
		AUTOTHROTTLE_START_DELAY=5.0,   # 最初的下载延迟（以秒为单位）
		AUTOTHROTTLE_MAX_DELAY=60.0, 	# 在高延迟情况下设置的最大下载延迟（以秒为单位）
		AUTOTHROTTLE_DEBUG=True,   	# 启用 AutoThrottle 调试模式，该模式显示收到的每个响应的统计数据，以便可以实时调节参数
		# AUTOTHROTTLE_TARGET_CONCURRENCY = 10, Scrapy 应平行发送到远程网站的请求数量 将此选项设置为更高的值以增加吞吐量和远程服务器上的负载 将此选项设置为更低的值以使爬虫更保守和礼貌
		#HTTPERROR_ALLOWED_CODES=[302, 500, 502, 404, 403, 503],
		# DOWNLOAD_DELAY=1,
		DOWNLOAD_TIMEOUT=120.0,
		# LOG_LEVEL='DEBUG',
		ITEM_PIPELINES={
			'scrapy_request.pipelines.BusinessPipeline': 300,
			'scrapy_request.pipelines.XinBDRedisPipeline': 301
		}
	)
	
	def __init__(self):
		self.base_url = "https://xin.baidu.com"
		self.first_base_url = "https://xin.baidu.com/s?q={}&t=0"
		self.pid_pattern = r'"pid":(.*?)\,.*?"defTags"'
		self.attr_pattern = r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)"
		self.mix_pattern = r'mix\((.*?)\(function'
		self.company_queue = "company_queue"
		self.fail_queue = "fail_queue"
		self.pattern_302 = re.compile(r".*?fromu=(.*?)$")		# 用来处理302跳转后的url重新抽取出来请求
		self.proxies = Proxies(get_redis_cli())					# 代理类,用来处理代理
		self.proxies_value = self.proxies.get_proxies()			# 用来标示单个线程IP值
		self.event = Event()									# 设置多线程下的事件锁
		self.event_flg = 1										# 用来标识第一个线程
		self.headers = {
			'Accept': "application/json, text/javascript, */*; q=0.01",
			'Accept-Encoding': "gzip, deflate, br",
			'Accept-Language': "zh-CN,zh;q=0.9",
			'Connection': "keep-alive",
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
			'Upgrade-Insecure-Requests': "1",
		}

	# @classmethod
	# def from_crawler(cls, crawler, *args, **kwargs):
	# 	spider = cls(*args, **kwargs)
	# 	spider._set_crawler(crawler)
	# 	return spider

	# twisted 异步请求异常捕获函数
	def errback_twisted(self, failure):
		if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
			request = failure.request
			company_name = request.meta["company_name"]
			self.server.rpush(self.company_queue, company_name)
		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response
			request = failure.value.request
			company_name = request.meta["company_name"]
			self.server.rpush(self.company_queue, company_name)

	def start_requests(self):
		# 根据企业名录拼接 url 获取到详情页 url，保存到 redis 中
		length = self.server.llen(self.company_queue)
		while True:
			company_name = self.server.lpop(self.company_queue)
			if company_name:
				company_name = company_name.decode("utf-8")
				uri = self.first_base_url.format(parse.quote(company_name))
				yield scrapy.Request(uri, headers=self.headers, meta={"company_name": company_name}, callback=self.parse, errback=self.errback_twisted)
			else:
				break
	
	def get_uri(self, d, text):
		pid = eval(re.findall(self.pid_pattern, text, re.S)[0])
		id1, att = re.findall(self.attr_pattern, text)[0]
		tk_func = "function mix(" + re.findall(self.mix_pattern, text, re.S)[0]
		'//*[@id="baiducode"]/text()'
		tk = re.findall(att + r'="(.*?)">', text)[0]
		tk = execjs.compile(tk_func).call('mix', tk, d)
		return pid, tk
	
	def parse(self, response):
		company_name=response.meta["company_name"]
		flg = response.xpath('//a[@title="{}"and@class="zx-list-item-url"]/@href'.format(company_name))
		if flg:
			uri = parse.urljoin(self.base_url, flg.extract_first())
			#  请求详情页面 url, 从详情页抽取出关键字段执行js获取到工商数据的url
			yield scrapy.Request(uri, headers=self.headers, callback=self.get_result_url, meta=response.meta, errback=self.errback_twisted)
		else:
			# 没有信息的公司,进行保存
			self.server.rpush("no_msg_queue", company_name)
			return

	def get_result_url(self, response):
		d = response.xpath('//*[@id="baiducode"]/text()').extract_first()
		pid, tk = self.get_uri(d, response.text)
		time1 = int(time.time() * 1000)
		uri = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
		# 请求上述 url, 获取到数据入库
		yield scrapy.Request(uri, headers=self.headers, callback=self.parse_result, meta=response.meta, errback=self.errback_twisted)
	
	def parse_result(self, response):
		# 解析数据
		html = json.loads(response.body.decode('unicode_escape'), strict=False).get("data")
		# item = BusinessItem()
		# # 统一社会信用代码/注册号
		# item["regNo"] = data.setdefault("regNo") if data.get("regNo") else "null"
		# # 组织机构代码
		# item["orgNo"] = data.setdefault("orgNo") if data.get("orgNo") else "null"
		# # 税务登记证号
		# item["taxNo"] = data.setdefault("taxNo") if data.get("taxNo") else "null"
		# # 百度信用代码
		# item["bdCode"] = data.setdefault("bdCode") if data.get("bdCode") else "null"
		# # 法定代表人
		# item["legalPerson"] = data.setdefault("legalPerson") if data.get("legalPerson") else "null"
		# # 经营状态
		# item["openStatus"] = data.setdefault("openStatus") if data.get("openStatus") else "null"
		# # 成立日期
		# item["startDate"] = data.setdefault("startDate") if data.get("startDate") else "null"
		# # 营业期限
		# item["openTime"] = data.setdefault("openTime") if data.get("openTime") else "null"
		# # 审核/年检日期
		# item["annualDate"] = data.setdefault("annualDate") if data.get("annualDate") else "null"
		# # 注册资本
		# item["regCapital"] = data.setdefault("regCapital") if data.get("regCapital") else "null"
		# # 企业类型
		# item["entType"] = data.setdefault("entType") if data.get("entType") else "null"
		# # 机构类型
		# item["orgType"] = data.setdefault("orgType") if data.get("orgType") else "null"
		# # 所属行业
		# item["industry"] = data.setdefault("industry") if data.get("industry") else "null"
		# # 行政区划
		# item["district"] = data.setdefault("district") if data.get("district") else "null"
		# # 登记机关
		# item["authority"] = data.setdefault("authority") if data.get("authority") else "null"
		# # 电话号码
		# item["telephone"] = data.setdefault("telephone") if data.get("telephone") else "null"
		# # 所在地址
		# item["regAddr"] = data.setdefault("regAddr") if data.get("regAddr") else "null"
		# # 经营范围
		# item["scope"] = data.setdefault("scope") if data.get("scope") else "null"
		# # 股东信息 - name, gender, title, img
		# item["directors"] = data.setdefault("directors") if data.get("directors") else "null"
		# # 主要人员 - name,type,img, amount
		# item["shares"] = data.setdefault("shares") if data.get("shares") else "null"
		# yield item
		# 解析详情拿到所有的详情二进制字符串
		item = XinbdItem()

		item['search_kw'] = response.meta['company_name']

		if 'entLogo' in html:
			item['entLogo'] = html['entLogo']
		else:
			item['entLogo'] = default_value

		if 'shareLogo' in html:
			item['shareLogo'] = html['shareLogo']
		else:
			item['shareLogo'] = default_value

		if 'entName' in html:
			item['entName'] = html['entName']
		else:
			item['entName'] = default_value

		if 'bdCode' in html:
			item['bdCode'] = html['bdCode']
		else:
			item['bdCode'] = default_value

		if 'openStatus' in html:
			item['openStatus'] = html['openStatus']
		else:
			item['openStatus'] = default_value

		if 'entType' in html:
			item['entType'] = html['entType']
		else:
			item['entType'] = default_value

		if 'isClaim' in html:
			item['isClaim'] = html['isClaim']
		else:
			item['isClaim'] = default_value

		if 'claimUrl' in html:
			item['claimUrl'] = html['claimUrl']
		else:
			item['claimUrl'] = default_value

		if 'benchMark' in html:
			item['benchMark'] = html['benchMark']
		else:
			item['benchMark'] = default_value

		if 'regNo' in html:
			item['regNo'] = html['regNo']
		else:
			item['regNo'] = default_value

		if 'orgNo' in html:
			item['orgNo'] = html['orgNo']
		else:
			item['orgNo'] = default_value

		if 'taxNo' in html:
			item['taxNo'] = html['taxNo']
		else:
			item['taxNo'] = default_value

		if 'scope' in html:
			item['scope'] = html['scope']
		else:
			item['scope'] = default_value

		if 'regAddr' in html:
			item['regAddr'] = html['regAddr']
		else:
			item['regAddr'] = default_value

		if 'legalPerson' in html:
			item['legalPerson'] = html['legalPerson']
		else:
			item['legalPerson'] = default_value

		if 'startDate' in html:
			item['startDate'] = html['startDate']
		else:
			item['startDate'] = default_value

		if 'openTime' in html:
			item['openTime'] = html['openTime']
		else:
			item['openTime'] = default_value

		if 'annualDate' in html:
			item['annualDate'] = html['annualDate']
		else:
			item['annualDate'] = default_value

		if 'regCapital' in html:
			item['regCapital'] = html['regCapital']
		else:
			item['regCapital'] = default_value

		if 'industry' in html:
			item['industry'] = html['industry']
		else:
			item['industry'] = default_value

		if 'telephone' in html:
			item['telephone'] = html['telephone']
		else:
			item['telephone'] = default_value

		if 'district' in html:
			item['district'] = html['district']
		else:
			item['district'] = default_value

		if 'authority' in html:
			item['authority'] = html['authority']
		else:
			item['authority'] = default_value

		if 'realCapital' in html:
			item['realCapital'] = html['realCapital']
		else:
			item['realCapital'] = default_value

		if 'orgType' in html:
			item['orgType'] = html['orgType']
		else:
			item['orgType'] = default_value

		if 'scale' in html:
			item['scale'] = html['scale']
		else:
			item['scale'] = default_value

		if 'directors' in html:
			item['directors'] = html['directors']
		else:
			item['directors'] = default_value

		if 'shares' in html:
			item['shares'] = html['shares']
		else:
			item['shares'] = default_value

		if 'districtCode' in html:
			item['districtCode'] = html['districtCode']
		else:
			item['districtCode'] = default_value

		if 'cid' in html:
			item['cid'] = html['cid']
		else:
			item['cid'] = default_value

		if 'website' in html:
			item['website'] = html['website']
		else:
			item['website'] = default_value

		if 'official_flag' in html:
			item['official_flag'] = html['official_flag']
		else:
			item['official_flag'] = default_value

		if 'shidi_pic' in html:
			item['shidi_pic'] = html['shidi_pic']
		else:
			item['shidi_pic'] = default_value

		if 'gongzhonghao' in html:
			item['gongzhonghao'] = html['gongzhonghao']
		else:
			item['gongzhonghao'] = default_value

		if 'xiongzhanghao' in html:
			item['xiongzhanghao'] = html['xiongzhanghao']
		else:
			item['xiongzhanghao'] = default_value

		if 'weibo' in html:
			item['weibo'] = html['weibo']
		else:
			item['weibo'] = default_value

		if 'phoneArr' in html:
			item['phoneArr'] = html['phoneArr']
		else:
			item['phoneArr'] = default_value

		if 'baozhang_flag' in html:
			item['baozhang_flag'] = html['baozhang_flag']
		else:
			item['baozhang_flag'] = default_value

		if 'shidi_flag' in html:
			item['shidi_flag'] = html['shidi_flag']
		else:
			item['shidi_flag'] = default_value

		if 'zixin_flag' in html:
			item['zixin_flag'] = html['zixin_flag']
		else:
			item['zixin_flag'] = default_value

		if 'chengqi_flag' in html:
			item['chengqi_flag'] = html['chengqi_flag']
		else:
			item['chengqi_flag'] = default_value

		if 'v_level' in html:
			item['v_level'] = html['v_level']
		else:
			item['v_level'] = default_value

		if 'v_url' in html:
			item['v_url'] = html['v_url']
		else:
			item['v_url'] = default_value
		yield item
