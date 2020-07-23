# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyRequestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ResultItem(scrapy.Item):
    # 商标名称
    tm_name = scrapy.Field()
    # 公众号名称
    public_name = scrapy.Field()
    # 微信号
    weChat = scrapy.Field()
    # 注册主体
    RegName = scrapy.Field()
    # 注册时间
    RegTime = scrapy.Field()
    # 头条阅读平均值
    TopReadNumAvg = scrapy.Field()
    # 原创比例
    OriginalProportion = scrapy.Field()
    # 功能介绍
    description = scrapy.Field()
    # TAG
    tag = scrapy.Field()
    # 头条\二条|三条全部篇数
    ArticleCount = scrapy.Field()
    # 阅读平均
    ReadNumAvg = scrapy.Field()
    # 阅读最高
    ReadNumMax = scrapy.Field()
    # 点赞平均
    LikeNumAvg = scrapy.Field()
    # 点赞最高
    LikeNumMax = scrapy.Field()
    # 文章热词前10
    TopWords = scrapy.Field()


class BusinessItem(scrapy.Item):
    # 统一社会信用代码/注册号
    regNo = scrapy.Field()
    # 组织机构代码
    orgNo = scrapy.Field()
    # 税务登记证号
    taxNo = scrapy.Field()
    # 百度信用代码
    bdCode = scrapy.Field()
    # 法定代表人
    legalPerson = scrapy.Field()
    # 经营状态
    openStatus = scrapy.Field()
    # 成立日期
    startDate = scrapy.Field()
    # 营业期限
    openTime = scrapy.Field()
    # 审核/年检日期
    annualDate = scrapy.Field()
    # 注册资本
    regCapital = scrapy.Field()
    # 企业类型
    entType = scrapy.Field()
    # 机构类型
    orgType = scrapy.Field()
    # 所属行业
    industry = scrapy.Field()
    # 行政区划
    district = scrapy.Field()
    # 登记机关
    authority = scrapy.Field()
    # 电话号码
    telephone = scrapy.Field()
    # 所在地址
    regAddr = scrapy.Field()
    # 经营范围
    scope = scrapy.Field()
    # 股东信息 - name, gender, title, img
    directors = scrapy.Field()
    # 主要人员 - name,type,img, amount
    shares = scrapy.Field()


class XinbdItem(scrapy.Item):
    # (entLogo, shareLogo, entName, bdCode, openStatus, entType, isClaim, claimUrl, benchMark, regNo, orgNo,
    #  taxNo, scope, regAddr, legalPerson, startDate, openTime, annualDate, regCapital, industry, telephone,
    #  district, authority, realCapital, orgType, scale, directors, shares, districtCode, cid, website,
    #  official_flag, shidi_pic, gongzhonghao, xiongzhanghao, weibo, phoneArr, baozhang_flag, shidi_flag,
    #  zixin_flag, chengqi_flag, v_level, v_url)
    search_kw = scrapy.Field()
    entLogo = scrapy.Field()
    shareLogo = scrapy.Field()
    entName = scrapy.Field()
    pid = scrapy.Field()
    tot = scrapy.Field()
    bdCode = scrapy.Field()
    openStatus = scrapy.Field()
    entType = scrapy.Field()
    isClaim = scrapy.Field()
    claimUrl = scrapy.Field()
    benchMark = scrapy.Field()
    regNo = scrapy.Field()
    orgNo = scrapy.Field()
    taxNo = scrapy.Field()
    scope = scrapy.Field()
    regAddr = scrapy.Field()
    legalPerson = scrapy.Field()
    startDate = scrapy.Field()
    openTime = scrapy.Field()
    annualDate = scrapy.Field()
    regCapital = scrapy.Field()
    industry = scrapy.Field()
    telephone = scrapy.Field()
    district = scrapy.Field()
    authority = scrapy.Field()
    realCapital = scrapy.Field()
    orgType = scrapy.Field()
    scale = scrapy.Field()
    directors = scrapy.Field()
    shares = scrapy.Field()
    districtCode = scrapy.Field()
    cid = scrapy.Field()
    website = scrapy.Field()
    official_flag = scrapy.Field()
    shidi_pic = scrapy.Field()
    gongzhonghao = scrapy.Field()
    xiongzhanghao = scrapy.Field()
    weibo = scrapy.Field()
    phoneArr = scrapy.Field()
    baozhang_flag = scrapy.Field()
    shidi_flag = scrapy.Field()
    zixin_flag = scrapy.Field()
    chengqi_flag = scrapy.Field()
    v_level = scrapy.Field()
    v_url = scrapy.Field()