import requests,re
from lxml import etree
import scrapy
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

''' 国家税务局(法人) '''
# class XXK_FRSpider(scrapy.Spider):
#
#     name = 'xxkFr'
#
#     def start_requests(self):
#         '''
#         给出每个关键字的URL，获取响应内容
#         :return:
#         '''
#         print('start crawl')
#         url = 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do'
#         datas={
#             'categeryid': '24',
#             'querystring24': 'articlefield02',
#             'querystring25': 'articlefield02',
#             'queryvalue': '赵'
#         }
#         headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#             'Connection': 'keep-alive',
#             'Host': 'hd.chinatax.gov.cn',
#             'Origin': 'http://hd.chinatax.gov.cn',
#             'Referer': 'http://hd.chinatax.gov.cn/xxk/',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#             'Cookie': 'qd80-cookie=qdyy34-80; qd80-cookie=qdyy34-80; yfx_c_g_u_id_10003701=_ck18121809095011130123672068273; JSESSIONID=eW3LYuefMuEKZTm3QadGl46V3OpR3MGjCWAyyHyZqGXjkdcW8RE1!377127501; yfx_f_l_v_t_10003701=f_t_1545095390100__r_t_1545303264541__v_t_1545303264541__r_c_2; _Jo0OQK=5134482794307ED550869A59340EF7A2C3C5BA41D23C0C35ACD359456BC282EB82659D242CF0065B393BB00ACF59DD8637FFD76B246166DE05CF34086A8BC0260151B918CCA8FE3BB942ACFE09BE178B5EF70EE0D297309F840EAD0449BC12889DF9A1B65BBEF8461DBGJ1Z1ag=='
#         }
#         yield scrapy.FormRequest(url,formdata=datas,headers=headers,callback=self.detailUrl_parse)
#
#     def detailUrl_parse(self,response):
#         '''
#         解析响应，获取 详情页的url，并发送请求
#         :param response:
#         :return:
#         '''
#         print('start parse')
#         print(response.status)
#         print(response.text)
#         links = response.xpath('//td[@bgcolor="#F0F0F0"]/a/@href').extract()
#         print(links)
#         for link in links:
#             link = 'http://hd.chinatax.gov.cn/xxk/action/'+ link
#             print(link)
#             headers = {
#                     'Connection': 'keep-alive',
#                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                     'Cookie': 'qd80-cookie=qdyy34-80; qd80-cookie=qdyy34-80; yfx_c_g_u_id_10003701=_ck18121809095011130123672068273; JSESSIONID=eW3LYuefMuEKZTm3QadGl46V3OpR3MGjCWAyyHyZqGXjkdcW8RE1!377127501; yfx_f_l_v_t_10003701=f_t_1545095390100__r_t_1545303264541__v_t_1545303264541__r_c_2; _Jo0OQK=7974482794307ED550869A59340EF7A2C3C5BA41D23C0C35ACD359456BC282EB82659D242CF0065B393BB00ACF59DD8637FFD76B246166DE05CF34086A8BC0260151B918CCA8FE3BB942ACFE09BE178B5EF70EE0D297309F840EAD0449BC12889DF9A1B65BBEF8461DBGJ1Z1Jw==',
#                     'Host': 'hd.chinatax.gov.cn',
#                     'Referer': 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do',
#                     'Upgrade-Insecure-Requests': '1',
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#                 }
#             yield scrapy.Request(link,headers=headers,callback=self.detail_parse)
#
#
#
#     def detail_parse(self,response):
#         '''
#         解析列表页，拿到详情
#         :param response:
#         :return:
#         '''
#         content = response.text
#         print(content)
#         info = content.xpath('')



url = 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do'
datas={
    'categeryid': '24',
    'querystring24': 'articlefield02',
    'querystring25': 'articlefield02',
    'queryvalue': '赵'
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'hd.chinatax.gov.cn',
    'Origin': 'http://hd.chinatax.gov.cn',
    'Referer': 'http://hd.chinatax.gov.cn/xxk/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla / 5.0(compatible;MSIE9.0;WindowsNT 6.1;Trident / 5.0',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
}
proxies = {
    "http" : "http://115.224.68.24:2314"   # 代理ip
}

res = requests.post(url,data=datas,headers=headers,proxies=proxies)
cookies = requests.utils.dict_from_cookiejar(res.cookies)
response = requests.post(url,data=datas,headers=headers,proxies=proxies,cookies=cookies).text
print(response)
html = etree.HTML(response)
page = html.xpath('//td[@valign="bottom"]/text()')[0][5]    # 页数
links = html.xpath('//td[@bgcolor="#F0F0F0"]/a/@href')    # 详情页的链接
for link in links:
    link = 'http://hd.chinatax.gov.cn/xxk/action/'+link
    print(link)
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'hd.chinatax.gov.cn',
        'Referer': 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'User-Agent': 'Mozilla / 5.0(compatible;MSIE9.0;WindowsNT 6.1;Trident / 5.0'
    }
    detail_info = requests.get(link,headers=headers,proxies=proxies,cookies=cookies).text
    # print(detail_info)
    tdList = re.findall(r'<td[^>]*>(.*?)</td>', html, re.I | re.M)
    # print(tdList)
    tdList1 = []
    for td in tdList:
        td.replace('<br>','、')
        tdList1.append(td)
    keys = tdList1[0::2]
    values = tdList1[1::2]
    # print('#####',keys)
    # print('#####',values)
    info = dict(zip(keys, values))
    print(info)