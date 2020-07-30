import requests,json,pymysql,time,random,string,uuid


class MyMysql():

    def __init__(self,AFF_ID):
        self.conn = pymysql.Connect('rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com', 'ddjuser', '3dIrM#sA@MA$x4aKGB', 'ddj')
        self.cursor = self.conn.cursor()
        self.AFF_ID=AFF_ID

    def query_all(self):
        querySql = "select offer_id from offer where aff_id = %s"
        self.cursor.execute(querySql,[self.AFF_ID])
        all_data = self.cursor.fetchall()
        return all_data

    def insert_one(self, offer_info):
        offer_id, offer_name, app_id, tracking_link, type, country, category, platform, status,creat_date, expire_date,\
        conversion_point, detail_info =offer_info
        insertSql = "insert into offer (offer_id,offer_name,app_id,tracking_link,`type`,country,category,platform,status,creat_date," \
                  "expire_date,events,other,aff_code, aff_id) Values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                  "'{}','{}')" .format(offer_id, offer_name, app_id, tracking_link, type, country, category,
                                                           platform, status,creat_date, expire_date,conversion_point, detail_info, 'filex', self.AFF_ID)
        self.cursor.execute(insertSql)
        self.conn.commit()

    def update_status(self, offer_id):
        updateStatusSql  ="update offer set status = 0 where offer_id = %s and aff_id = %s"
        self.cursor.execute(updateStatusSql,[offer_id, self.AFF_ID])
        self.conn.commit()

    def update_one(self, offer_info):
        offer_id, offer_name, app_id, tracking_link, type, country, category, platform, status, creat_date, expire_date, \
        conversion_point, detail_info = offer_info
        updateSql = "UPDATE offer set offer_id = '{}',offer_name = '{}',app_id = '{}',tracking_link = '{}',`type` = '{}'," \
                    "country = '{}',category = '{}',platform = '{}',status = '{}',creat_date = '{}',expire_date = '{}'," \
                    "events = '{}',other = '{}', aff_code = '{}',aff_id = '{}'where offer_id = '{}'".format(offer_id, offer_name,
                    app_id, tracking_link, type, country, category,platform, status,creat_date, expire_date, conversion_point,
                    detail_info, 'filex',self.AFF_ID, offer_id)
        self.cursor.execute(updateSql)
        self.conn.commit()

    def conn_close(self):
        self.cursor.close()
        self.conn.close()

'''---------------------------------------检查offer中的url跳转5次就丢弃，用的ip代理---------------------------------------------'''
def get_ip(country):
    db = pymysql.connect("rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com", "ddjuser", "3dIrM#sA@MA$x4aKGB","ddj")
    # ip；用户名；密码；数据库
    db.ping(reconnect=True)
    cursor = db.cursor()
    while 1:
        # ip_sql = "SELECT Country, GROUP_CONCAT(ip),GROUP_CONCAT(Port) FROM ipproxy WHERE Status = 1 GROUP BY Country"
        ip_sql = "SELECT Ip,Port FROM ipproxy WHERE Status = 1 and Country = '{}'".format(country)
        cursor.execute(ip_sql)
        ips_info = cursor.fetchall()
        cursor.close()
        db.close()
        return ips_info

# device_offer_id=ifa；日志data的ifa
# ip,str(port)：mysql的ip,port
# template_url：mysql的url+'&aff_click_id=%s&sub_affid=%s&device_id=%s' % (str(uuid.uuid1()).upper(), sub_affid, ifa)
# ua：日志data的ua
# device_ip：日志data的ip
# '''
# :param device_offer_id:设备id
# :param ip:代理ip
# :param port:代理ip端口
# :param url:短链接
# :param ua:设备ua
# :param device_ip:设备ip
# :return:
# '''

def send_requests(ip, port, url, ua, device_ip):
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

    skip = 0
    while 1:
        if url.startswith('http'):
            try:
                if skip >= 5:
                    break
                r = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False, timeout=2)
                s = r.status_code
                # print(redirectNum)
                if s >= 300 and s <= 400:
                    h = r.headers
                    url = h['Location']
                    skip += 1
            except Exception:
                break
        else:
            break
    if skip >= 5:
        return 0
    else:
        return 1

'''------------------------------------'''
def check_offer_url(url, country):     #检查offer中的url是否可用，跳转5次就存
    sub_affids = [''.join(random.sample(string.digits+string.ascii_letters, 18)) for i in range(1500)]
    # url="http://filexmedia.fuse-cloud.com/tl?a=204&o=4065365"
    ifa = "f0e29e08-ab9f-4c26-b78a-20b50a2ebdde"
    # ips_info = usaip    #(('149.129.235.109', 8899), ('147.139.129.98', 8899), ('147.139.136.131', 8899), ('149.129.239.158', 8899))
    # ips_info = (('149.129.235.109', 8899), ('147.139.129.98', 8899), ('147.139.136.131', 8899), ('149.129.239.158', 8899))
    useip = get_ip(country)  # ip代理；需填入国家
    ua = "Mozilla/5.0 (Linux; Android 9; Redmi 6A Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36"
    device_ip = "36.75.142.210"
    '''------------------------------------'''
    sub_affid = random.sample(sub_affids, 1)[0]
    template_url = url + '&aff_click_id=%s&sub_affid=%s&device_id=%s' % (str(uuid.uuid1()).upper(), sub_affid, ifa)
    ip_port = random.sample(useip, 1)
    ip, port = ip_port[0]
    result=send_requests(ip, str(port), template_url, ua, device_ip)
    return result


'''-------------------------------------检查offer中的url跳转5次就不用，用的ip代理；结束块-----------------------------------------------'''


country_dict = {'IN':'IND','ID':'INA','KR':'KOR','JP':'JPN'}

def country_map(country):
    return country_dict.get(country, 'ALL')


def get_offer_info(API_Key,AFF_ID):
    url = 'http://filexmedia.fuseclick.com/api/v2/getOffers?key={API_Key}&a={AFF_ID}&limit=1000&page=1'.format(API_Key=API_Key, AFF_ID=AFF_ID)
    # print(url)
    response = requests.get(url)
    response=response.text
    dataList = json.loads(response)['data']['content']
    for data in dataList:
        offer_id = data['id']
        offer_name = data['name'].replace("'","") if "'" in data['name'] else data['name']
        app_id = data['app_id']  # package name

        '''------检查设备系统是否为android,不是直接跳过------'''
        if '.' not in app_id or 'ios' in offer_name.lower():
            continue

        status = 1 if data['status']=='Active' else 0
        tracking_link = data['tracking_link']
        type = data['type']
        platform = data.get('platform', 'all')
        country = data['geo_countries']

        '''------检查国家是否是印度或印度尼西亚,不是直接跳过------'''
        if AFF_ID == 204:
            country = country_map('ID') if 'ID' in country else country_map('IN') if 'IN' in country else 'other'

        '''------检查国家是否是日本或韩国,不是直接跳过------'''
        if AFF_ID == 215:
            country = country_map('JP') if 'JP' in country else country_map('KR') if 'KR' in country else 'other'

        if country == 'other' or country == 'TW':
            continue

        category = '' if data['categories'] == [] else ','.join(data['categories'])
        creat_date = data['create_date']
        expire_date = data['expire_date']
        conversion_point = data['events'][0]['conversion_point']
        detail_info = json.dumps(data).replace("\\","").replace("'","") if "\'" in json.dumps(data) else json.dumps(data)

        yield offer_id, offer_name, app_id, tracking_link, type, country, category, platform, status, creat_date, expire_date, conversion_point, detail_info

def loop(API_Key, AFF_ID):
    ms = MyMysql(str(AFF_ID))
    api = list(get_offer_info(API_Key, AFF_ID))
    db = [i[0] for i in ms.query_all()]
    api_offer_id = [j[0] for j in api]
    db_no = (x for x in api if x[0] not in db)
    api_no = (y for y in db if y not in api_offer_id)
    api_db = (z for z in api if z[0] in db)

    if db_no:
        print('insert')
        for offer_info in db_no:
            # print(offer_info)
            '''------检查该offer跳转少于5次就入库------'''
            check_result = check_offer_url(offer_info[3], offer_info[5])
            if not check_result:
                continue
            ms.insert_one(offer_info)

    if api_no:
        print('update status')
        for offer_id in api_no:
            # print(offer_id)
            ms.update_status(offer_id)

    if api_db:
        print('update offer')
        for offer_info in api_db:
            # print(offer_info)
            ms.update_one(offer_info)

    ms.conn_close()
    print(time.strftime('%Y-%m-%d %T'))

if __name__ == '__main__':
    '''日本, 韩国'''
    # API_Key='06745AF528A5FFF82C45E103F1F55129'
    # AFF_ID=215
    '''印度, 印尼'''
    # API_Key = '3E47E7F014A02A7D0DF0FBCD1A42994A'
    # AFF_ID = 204
    '''---------------------印度&印度尼西亚-------------------------------日本&韩国&台湾---------------------'''
    offers = [('3E47E7F014A02A7D0DF0FBCD1A42994A',204),('06745AF528A5FFF82C45E103F1F55129',215)]
    while 1:
        for offer_api in offers:
            loop(offer_api[0], offer_api[1])
        time.sleep(1200)