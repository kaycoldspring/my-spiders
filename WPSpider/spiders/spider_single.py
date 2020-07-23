# -*- coding: utf-8 -*-
# @Time    : 2020/7/18 14:24
# @Author  : Kay Luo
# @FileName: spider_single.py
# @Software: PyCharm

import scrapy, re, random
from lxml import etree
from ..items import WpspiderItem



default_value = ""
class SingleSpider(scrapy.Spider):
    name = 'single_spider'
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        super(SingleSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        myheaders = {
            'authority': self.url.split('/')[2],
            'path': '/' + '/'.join(self.url.split('/')[3:]),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept - encoding': 'gzip, deflate, br',
            'accept - language': 'zh - CN, zh;q = 0.9',
            'cache - control': 'max - age = 0',
            'referer': '/'.join(self.url.split('/')[0:-2]),
        }
        yield scrapy.Request(self.url, headers=myheaders, callback=self.detail_parse)

    def detail_parse(self, response):
        p_title = response.xpath('//h1/text()').extract()[0]
        try:
            p_price = response.xpath('//span[@class="price-item price-item--regular"]/text()').extract()[0]
        except IndexError:
            p_price = random.randint(50,100)
        try:
            p_category = response.xpath('//span[@class="posted_in"]/a/text()').extract()[0]
        except IndexError:
            p_category = 'Best Sale'
        try:
            p_tags = response.xpath('//span[@class="tagged_as"]/a[1]/text()').extract()[0]
        except IndexError:
            p_tags = default_value
        p_imgList = []
        lis = response.xpath('//*[@id="ProductSection-product-template"]/div/div[1]/div[15]/ul/li/a/img/@src | /html/body/main/div/div[1]/div[1]/div/div[1]/div/img/@src | //div[contains(@id,"ProductPhotos-")]/div/div/div/img/@data-photoswipe-src | //div[contains(@id,"Image")]/div/img/@src').extract()
        for img in lis:
            p_imgList.append('https:' + img)
        # pList = []
        try:
            div = etree.HTML(response.text).xpath('//div[@class="ProductMeta__Description Rte"] | //div[@class="description"] | //div[@class="product-description rte"] | //div[@class="ProductMeta__Description"]')[0]
        except IndexError:
            div = ""
        p_description = etree.tostring(div, encoding='utf-8')
        p_descriptionStr = str(p_description, encoding='utf-8')
        # pList.append(p_descriptionStr)
        pattern = re.compile(r'<div .*?>')
        # n1 = re.sub(pattern, '<div>', html)
        # print(n1)
        description = re.sub(pattern, '<div>', p_descriptionStr)
        imgs = ' | '.join(p_imgList)
        # print(p_title,p_price,p_category,p_tags,imgs)
        # print(p_description)
        item = WpspiderItem()
        item['p_title'] = p_title
        item['p_price'] = p_price
        item['p_category'] = p_category
        item['p_tags'] = p_tags
        item['p_description'] = description
        item['p_img'] = imgs
        yield item
