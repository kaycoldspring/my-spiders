import json
import requests


def get_proxies():
    """
    连接API获取付费的代理IP
    :return: 代理IP
    """
    # API 请求
    url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=3&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    # 发送请求获取响应
    results = requests.get(url).text.split()[0]
    result = {'ip_port':results}
    print("查看获取的响应：", result)
    return result
    # 获取的json,从中解析出IP，port
    # for result in results:
    #     ip = result['ip']
    #     port = result['port']
    #
    # return ip + ':' + port


if __name__ == "__main__":
    get_proxies()