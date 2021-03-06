import json,re,scrapy
from urllib import parse
from SXR.get_page import get_page
from SXR.items import SxrItem
from scrapy_redis.spiders import RedisSpider
from SXR.get_conn import MyMysqlClient


''' 
爬取失信被执行人
        1.手动访问网站，F12分析网页，发现数据是隐藏在js里
        2.拿到数据对应的url，请求方式为GET，需要参数，响应内容为js，内容格式为字符串，
          分析URL的参数，发现只有pn和iname的值变化，所以这两项不能写死，要动态变化
        3.通过测试可知，需要加headers，发送请求
        4.拿到相应内容后解析，并存储
'''

# with open('GB2312汉字.txt','r') as f:
#     words = f.read()

class BaidusxrSpider(RedisSpider):

    name = 'sxr1'
    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "DOWNLOAD_DELAY": 3,
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",  # 分布式调度器
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",  # 分布式去重
        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderQueue",  # 队列形式，请求先进先出
        "SCHEDULER_PERSIST": True,  # 允许暂停，redis请求记录不丢失
        "COOKIES_ENABLED": False,  # 禁用 cookie
        "REDIRECT_ENABLED": False,  # 禁用重定向
        "REDIS_HOST": '172.16.51.113',
        "REDIS_PORT": '8000',
        "REDIS_PARAMS": {
            'password': '',
            'db': 2
        },
        "DOWNLOADER_MIDDLEWARES": {
            'SXR.middlewares.ProxyMiddleware': 125,
            'SXR.middlewares.Uamid': 1,
        },
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 2,
        "ITEM_PIPELINES": {
            'SXR.pipelines.SxrPipeline': 300,
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    def __init__(self,pc=None,*args,**kwargs):
        self.db = MyMysqlClient()
        # self.flag = False
        if pc == None:
            self.pc =pc
            # self.flag = True
        else:
            self.pc = pc
        super(BaidusxrSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        '''
        给定起始URL，拿到响应内容
        :return:
        '''
        for results in get_page():
            for result in results:
                for page in range(results[result]):
                    print('当前关键字为%s'%result)
                    print('对应页数为%s'%str(page))
                    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?' \
                          'resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&' \
                          'cardNum=&iname='+parse.quote(result)+'&areaName=&pn='+str(page * 10)+'&rn=10&ie=utf-8&oe=utf-8&format=json&t=1544166746191&' \
                          'cb=jQuery110201855220806143778_1544146123535&_=1544146123629'
                    headers = {
                        'Accept': ' * / *',
                        'Connection': 'keep - alive',
                        'Host': 'sp0.baidu.com',
                        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=92495750_hao_pg&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&'
                                   'rsv_pq=a7fd7e6400019288&rsv_t=62cfttvGmYTkabqLarrpEkV9w%2FOt11rbAGfmEkmOcbShE9krvXVR6tYF9l%2FBh1ZAuyCa8mx3&'
                                   'rqlang=cn&rsv_enter=1&rsv_sug3=8&rsv_sug2=0&inputT=1289&rsv_sug4=1290'
                    }
                    yield scrapy.Request(url,headers=headers,callback=self.detail_parse)
                self.db.save_word(result)

    def detail_parse(self,response):
        '''
        解析js，转成json，获取数据
        :return:
        '''
        content = response.text
        # print(content)
        '''拿到content，类型是一个字符串，用正则匹配出数据所在的{}，
        其内容为列表，列表里又有{}，遍历拿到{}，并用json转成字典'''

        p = re.compile(r'[(](.*)[)]', re.S)
        datas = re.findall(p, content)
        for data in datas:
            # print(data)
            # 转成字典后，通过键和下标取出数据所在的result
            try :
                infos = json.loads(data)['data'][0]['result']
                for info in infos:
                    del info['SiteId']
                    del info['StdStg']
                    del info['StdStl']
                    del info['_select_time']
                    del info['_update_time']
                    del info['_version']

                    '''如果存入关系型数据库的话，那么这里的字段和pipeline里的字段保持一致即可，
                    但由于要存json文件，所以这里把数据存放在字典中，然后在pipeline中转成json格式'''

                    # 为了确定每条数据是惟一的，定义独有的key
                    # detailKey = info['iname'] + '@'+ info['cardNum'] +'@'+ info['caseCode']
                    # detail = {}
                    # # 最后将key和value一起存入字典
                    # detail.update({detailKey:info})
                    # print(detail)

                    '''导入item'''
                    item = SxrItem()
                    item['informations'] = info
                    yield item
            except IndexError:
                pass






