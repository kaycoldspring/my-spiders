from fake_useragent import UserAgent

# http://h.zhimaruanjian.com
# 18518075890  1qaz2wsX

def get_ua():
    '''
    获取随机的user-agent
    :return:
    '''
    ua = UserAgent().random
    print('已取得用户代理：%s'%ua)
    return ua


def get_proxies():
    '''
    获取代理ip
    :return:
    '''
    pass