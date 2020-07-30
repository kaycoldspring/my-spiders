# -*- coding:utf-8 -*-
import string
from queue import Queue
import pymysql, sys, os
import requests
import uuid, random, json, time
import threading, datetime
from pymongo import MongoClient
from dateutil.parser import parse


ifa_dict = {'ios': 'idfa=', 'android': 'gaid='}

# username = parse.quote_plus('root')
# password = parse.quote_plus('3dIrM#sA@MA$x4aKGB')
# myclient = MongoClient(
#     'mongodb://{0}:{1}@dds-a2d7764c4ba4da841.mongodb.ap-south-1.rds.aliyuncs.com:3717/'.format(username, password))
myclient = MongoClient(host='dds-a2d7764c4ba4da841.mongodb.ap-south-1.rds.aliyuncs.com',port=3717,username='root',password='3dIrM#sA@MA$x4aKGB',
                       minPoolSize=300,maxPoolSize=500)
mydb = myclient["OFFER_4"]
mycol = mydb['POSTED_1']
# mycol.create_index("name", unique=True)

detected_offer = set([])
offers_info = ()
ips_info = []
sub_affids = [''.join(random.sample(string.digits+string.ascii_letters, 18)) for i in range(1500)]


def query(device_offer_id):
    res = mycol.find_one({"name":device_offer_id})
    # print(res)
    if res:
        # print('有记录:', res)
        # for x in res:
        post_time = res.get("value")
        # print(post_time)
        if int(time.time()) - post_time >= 3600:
            return 1
        else:
            return 0
    else:
        return 1


def add(device_offer_id):
    post_time = int(time.time())
    data_dict = {"value" : post_time}
    mycol.update_one({"name" : device_offer_id},{"$set" : data_dict},True)



def send_requests(device_offer_id, ip, port, url, ua, device_ip):
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
                    r = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False)
                    s = r.status_code
                    redirectNum += 1
                    if s >= 300 and s <= 400:

                        h = r.headers
                        url = h['Location']
                        link_list.append(url)
                    else:
                        break
                        # print(url)
                except Exception as e:

                    break


            else:
                break
        if len(link_list) > 0:
            last_link = link_list[-1]
        else:
            last_link = url
        t = time.time()
        print('used time:',t-t0,'    last_link:',last_link)
        # print(url, 'responded')
        # print('跳转次数:', redirectNum)

        return 1
    else:
        # print('needexe = 0 ', device_offer_id)
        return 0

def get_detect_resp(offer_info):  # 参数为offer信息,是一个数�?
    global ips_info

    offer_id, platform, country, url, app_id, ifa, id, ua, device_ip = offer_info
    # sub_affid = ''.join(random.sample(string.digits, 10))
    # sub_affid = str(1000 + random.randint(0, 51))
    sub_affid = random.sample(sub_affids, 1)[0]
    template_url = url + '&aff_click_id=%s&sub_affid=%s&device_id=%s' % (str(uuid.uuid1()).upper(), sub_affid, ifa)
    # 发请求之前查询是否mongoDB中是否已有记录
    device_offer_id = ifa
    # return c

    ip_port = random.sample(ips_info, 1)
    ip, port = ip_port[0]
    # print('ip:',ip, port)
    # t3 = time.time()
    send_requests(device_offer_id, ip, port, template_url, ua, device_ip)
    # t4 = time.time()
    # print('get_detect_resp:',t4-t3)


def close_mysql(db,cursor):
    db.close()
    cursor.close()


def get_offer_detect_data(link_list):
    for offer_info in link_list:
        get_detect_resp(offer_info)


def detect_offer(line):
    global  offers_info
    if '<deal_device' in line:
        try:
            line = line[81:-2]
            data = json.loads(line)
        except Exception:
            return
    elif 'body:{' in line:
        try:
            line = line[74:-2]
            data = json.loads(line)['device']
            # print('device:', data)
        except Exception:
            return
    else:
        return

    ifa = data.get('ifa', '')
    ua = data['ua']
    device_ip = data.get('ip')
    # print(geo, device, ifa, ua)
    needexe = query(ifa)
    if needexe == 1:
        try:
            detect_list = [[d[0], d[1], d[2], d[3], d[4], ifa, d[5], ua, device_ip] for d in offers_info if
                           d[0] not in detected_offer]
            get_offer_detect_data(detect_list)
            add(ifa)
            return
        except Exception as e:
            print('error reason:', e)
    else:
        return


def get_offer_info(country):
    global offers_info
    db = pymysql.connect("rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com", "ddjuser", "3dIrM#sA@MA$x4aKGB",
                         "ddj")
    db.ping(reconnect=True)
    cursor = db.cursor()
    while 1:
        sql = "select offer_id,platform,country,tracking_link,app_id,id from offer where status = 1 and " \
              "country like '%{geo}%' order by sort DESC ".format(geo=country)
        cursor.execute(sql)
        offers_info = cursor.fetchall()
        time.sleep(300)


def get_ip(country):
    global ips_info
    db = pymysql.connect("rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com", "ddjuser", "3dIrM#sA@MA$x4aKGB",
                         "ddj")
    db.ping(reconnect=True)
    cursor = db.cursor()
    while 1:
        # ip_sql = "SELECT Country, GROUP_CONCAT(ip),GROUP_CONCAT(Port) FROM ipproxy WHERE Status = 1 GROUP BY Country"
        ip_sql = "SELECT Ip,Port FROM ipproxy WHERE Status = 1 and Country = '{}'".format(country)
        cursor.execute(ip_sql)
        ips_info = cursor.fetchall()
        # ips_info_res = {}
        # for i in ip_info:
        #     dic = list(map(lambda x, y: [x, y], i[1].split(","), i[2].split(",")))
        #     ip_info_res[i[0]] = dic
        # ips_info = ip_info_res[random.sample(ip_info_res.keys(), 1)]
        # print('query db:',ips_info)
        time.sleep(120)


def worker():
    global data
    while True:
        line = queue.get()
        # print('work',i)
        if line:
            s = time.time()
            detect_offer(line)
            e = time.time()
            print('each time:',e-s)
        else:
            time.sleep(0.1)


if __name__ == '__main__':
    COUNTRY = "IND"

    start_n = int(sys.argv[1])
    end_n = int(sys.argv[2])

    s = time.time()
    # db, currsor = conncet_mysql()
    queue = Queue(400)

    file_finished = 0

    t2 = threading.Thread(target=get_offer_info, args=(COUNTRY,))
    t3 = threading.Thread(target=get_ip, args=(COUNTRY,))
    t2.start()
    t3.start()
    time.sleep(10)

    for i in range(200):
        t1 = threading.Thread(target=worker, args=())
        t1.start()


    time2 = time.time()
    rq = time.strftime("%Y-%m-%d")
    gt = parse(rq + ' 03:30:00')
    lt = parse(rq + ' 09:30:00')
    n = 0
    while 1 :
        files = os.listdir('/data/work')
        if len(files) > 0:
            with open('/data/work/'+ files[0]) as f:
                while 1:
                    NOW = datetime.datetime.now()
                    if NOW > gt and NOW < lt:
                        time.sleep(300)
                    else:
                        line = f.readline()
                        n += 1
                        if line == '':
                            break
                        if '"IND"' in line and 'Android' in line:
                            queue.put_nowait(line)
                        while queue.full():
                            time.sleep(0.1)

                        if n % 100 == 0:
                            print('filename:',files[0],'    readlines:',n)
            # shutil.move(r'/data/work/' + files[0], r'/data/detected/' + files[0])
            # file_finished = 1
            os.remove('/data/work/'+ files[0])
            time3 = time.time()
            print('all time:', time3 - time2)
        else:
            time.sleep(300)

