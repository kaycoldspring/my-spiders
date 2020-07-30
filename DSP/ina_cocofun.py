# -*- coding:utf-8 -*-
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import json, random, requests, uuid, pymysql
import logging, threading, os
import multiprocessing
from pymongo import MongoClient
import time, datetime, string
from dateutil.parser import parse
from logging.handlers import RotatingFileHandler



logger = logging.getLogger('INA')
logger.setLevel(logging.DEBUG)

# 建立一个FileHandler来把日志记录在文件里，级别为debug以上
fh = RotatingFileHandler("/DSP_data/logs/ina_click.log",maxBytes=1024*1024*100, backupCount=1)
fh.setLevel(logging.DEBUG)
# 建立一个StreamHandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)


COROUTINE_NUMBER = 1000  # 协程池数量
pool = Pool(COROUTINE_NUMBER)  # 使用协程池

# myclient = MongoClient(host='dds-k1a4c899a7d43dd41.mongodb.ap-southeast-5.rds.aliyuncs.com',port=3717,username='root',password='3dIrM#sA@MA$x4aKGB',
#                         minPoolSize=300,maxPoolSize=500)
# mydb = myclient["OFFER_4"]
# mycol = mydb['POSTED_1']
#mycol.create_index("name", unique=True)



class InaClick(object):

    def __init__(self):

        self.detect_offers = set([])
        self.offers_info = (('4721035', 'all', 'IDN', 'http://filexmedia.fuse-cloud.com/tl?a=204&o=4721035', 'com.yy.hiyo', 1153),)
        self.ips_info = ()
        self.sub_affids = [''.join(random.sample(string.digits+string.ascii_letters, 18)) for i in range(1500)]

    def query(self, device_offer_id):
        '''
        查询mongo中是否由此设备
        :param device_offer_id: 设备号
        :return: 1 --> 可以发   0 --> 不发
        '''
        # res = mycol.find_one({"name":device_offer_id})
        # if res:
        #     post_time = res.get("value")
        #     if int(time.time()) - post_time >= 3600 * 24:
        #         return 1
        #     else:
        #         return 0
        # else:
        #     return 1

    def add(self, device_offer_id):
        '''
        可以发的时候更新mongo
        :param device_offer_id: 设备号
        :return:
        '''
        post_time = int(time.time())
        # data_dict = {"value" : post_time}
        # mycol.update_one({"name" : device_offer_id},{"$set" : data_dict},True)

    def send_requests(self, device_offer_id, ip, port, url, ua, device_ip):
        '''
        发送请求
        :param device_offer_id: 设备号
        :param ip: ip地址
        :param port: 端口
        :param url: 请求url
        :param ua: 设备ua
        :param device_ip: 设备ip
        :return: 0 --> 无效的请求   1 --> 有效的请求
        '''
        if device_offer_id:
            t0 = time.time()
            headers = {
                'User-Agent': ua,
                'accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8, application/signed-exchange;v = b3',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'en-US',
                'X-Forwarded-For': device_ip,
                'Connection': 'close'
            }

            proxies = {
                'https': 'http://' + ip + ':' + port + '/',
                'http': 'http://' + ip + ':' + port + '/'
            }
            redirectNum = 0
            link_list = []
            s = 0
            while 1:
                if url.startswith('http'):
                    try:
                        if redirectNum > 5:
                            break
                        r = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False, timeout=2)
                        s = r.status_code
                        redirectNum += 1
                        if s >= 300 and s <= 400:
                            h = r.headers
                            url = h['Location']
                            link_list.append(url)
                    except Exception as e:
                        logger.error(e)
                        break

                else:
                    break
            if len(link_list) > 0:
                last_link = link_list[-1]
            else:
                last_link = url
            t = time.time()
            logger.info('current IP:%s      used time:%s    last_link:%s'%(ip, t - t0, last_link))
            return 1
        else:
            return 0

    def get_detect_resp(self, offer_info):
        '''
        处理offer数组
        :param offer_info: offer数组
        :return:
        '''
        offer_id, platform, country, url, app_id, ifa, id, ua, device_ip = offer_info
        sub_affid = random.sample(self.sub_affids,1)[0]
        # sub_affid = str(1000 + random.randint(0, 51))
        template_url = url + '&aff_click_id=%s&sub_affid=%s&device_id=%s' % (str(uuid.uuid1()).upper(), sub_affid, ifa)
        # 发请求之前查询是否mongoDB中是否已有记录
        device_offer_id = ifa
        # return c

        ip_port = random.sample(self.ips_info, 1)
        ip, port = ip_port[0]
        self.send_requests(device_offer_id, ip, str(port), template_url, ua, device_ip)

    def close_mysql(self, db, cursor):
        db.close()
        cursor.close()

    def get_offer_detect_data(self, link_list):
        for offer_info in link_list:
            if self.get_detect_resp(offer_info):
                break   # 如果offer已经被发过,则跳过

    def get_ip(self, country):
        '''
        获取ip
        :param country: 国家
        :return:
        '''
        db = pymysql.connect("rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com", "ddjuser", "3dIrM#sA@MA$x4aKGB",
                             "ddj")
        db.ping(reconnect=True)
        cursor = db.cursor()
        while 1:
            ip_sql = "SELECT Ip,Port FROM ipproxy WHERE Status = 1 and Country = '{}'".format(country)
            cursor.execute(ip_sql)
            self.ips_info = cursor.fetchall()

            time.sleep(120)

    def read_file(self, fname):
        """
        读取文件
        :param fname: 文件
        :return:
        """
        rq = time.strftime("%Y-%m-%d")
        gt = parse(rq + ' 02:00:00')
        lt = parse(rq + ' 08:00:00')
        with open(fname, encoding='utf-8') as f:
            NOW = datetime.datetime.now()
            if NOW > gt and NOW < lt:
                time.sleep(300)
            else:
                logger.info('start read')
                pool.map(self.detect_offer, f)

    def detect_offer(self, line):
        '''
        检测offer
        :param line: 带有设备号的日志  一行
        :return:
        '''
        if '"IDN"' in line and 'Android' in line:
            if '<deal_device' in line:
                try:
                    line = line[81:-2]
                    data = json.loads(line)
                    # print(data)
                except Exception as e:
                    logger.error(e)
                    return
            elif 'body:{' in line:
                try:
                    line = line[74:-2]
                    data = json.loads(line)['device']
                    # print(data)
                except Exception as e:
                    logger.error(e)
                    return
            else:
                return

            ifa = data.get('ifa', '')
            device_ip = data.get('ip')
            ua = data['ua']  # India
            # if self.query(ifa) == 1:
            try:
                detect_list = [[d[0], d[1], d[2], d[3], d[4], ifa, d[5], ua, device_ip] for d in self.offers_info if d[0] not in self.detect_offers]
                self.get_offer_detect_data(detect_list)
                # self.add(ifa)
                return
            except Exception as e:
                logger.error(e)
            # else:
            #     return
        else:
            logger.info('This device does not match the selected country')
            return

    def main(self):
        """
        使用多进程执行程序
        :return:r
        """
        # 文件列表
        start_time = time.time()

        COUNTRY = 'INA'
        t3 = threading.Thread(target=self.get_ip, args=(COUNTRY,))
        t3.start()
        time.sleep(10)

        while 1:
            pool = multiprocessing.Pool()
            files = os.listdir('/data/work')
            if len(files) > 0:
                for f in files:
                    file = '/data/work/' + f
                    logger.info('current file:%s'%file)
                    pool.apply_async(self.read_file, args=(file,))  # 子进程调用函数
                    os.remove(file)
                    # p.start()  # 启动进程
                    # logger.info('进程启动')
                    # p_list.append(p)  # 将所有进程写入列表中
                    #
                    # for p in p_list:
                    #     p.join()  # 检测p是否结束,如果没有结束就阻塞直到结束,否则不阻塞
                pool.close()
                pool.join()
                end_time = time.time()
                logger.info('all used time:%s'%(end_time - start_time))
                # shutil.move(files, r'/data/detected/' + file)

            else:
                logger.info('No executable file in the destination folder')
                time.sleep(300)



if __name__ == '__main__':
    InaClick().main()  # 启动主程序
