# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread


class ScrapyRequestPipeline(object):
    def __init__(self):
        self.serialize = ScrapyJSONEncoder().encode
    
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
    
    def _process_item(self, item, spider):
        key = "data_aiweibang"
        data = self.serialize(item)
        spider.server.rpush(key, data)
        return item


class BusinessPipeline(object):
    def __init__(self):
        self.serialize = ScrapyJSONEncoder().encode

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = "data_business"
        data = self.serialize(item)
        spider.server.rpush(key, data)
        return item


class XinBDRedisPipeline(object):

    def open_spider(self, spider):
        self.file = open('./info.txt', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        aim = dict(item)
        search_kw = str(aim['search_kw'])
        entLogo = str(aim['entLogo'])
        shareLogo = str(aim['shareLogo'])
        entName = str(aim['entName'])
        bdCode = str(aim['bdCode'])
        openStatus = str(aim['openStatus'])
        entType = str(aim['entType'])
        isClaim = str(aim['isClaim'])
        claimUrl = str(aim['claimUrl'])
        benchMark = str(aim['benchMark'])
        regNo = str(aim['regNo'])
        orgNo = str(aim['orgNo'])
        taxNo = str(aim['taxNo'])
        scope = str(aim['scope'])
        regAddr = str(aim['regAddr'])
        legalPerson = str(aim['legalPerson'])
        startDate = str(aim['startDate'])
        openTime = str(aim['openTime'])
        annualDate = str(aim['annualDate'])
        regCapital = str(aim['regCapital'])
        industry = str(aim['industry'])
        telephone = str(aim['telephone'])
        district = str(aim['district'])
        authority = str(aim['authority'])
        realCapital = str(aim['realCapital'])
        orgType = str(aim['orgType'])
        scale = str(aim['scale'])
        directors = aim['directors']
        # print(directors)
        # print(type(directors))
        # ls
        # parse_d = re.compile(r'{"name": "(.*?)", "gender": "(.*?)", "title": "(.*?)", "img": "(.*?)"}').findall(directors)
        directors_info = []
        for detail in directors:

            if 'name' in detail:
                directors_name = detail['name']
            else:
                directors_name = 'null'

            if 'gender' in detail:
                directors_gender = detail['gender']
            else:
                directors_gender = 'null'

            if 'title' in detail:
                directors_title = detail['title']
            else:
                directors_title = 'null'

            if 'img' in detail:
                directors_img = detail['img']
            else:
                directors_img = 'null'

            directors_info.append(directors_name + 'à' + directors_gender + 'à' + directors_title
                                                   + 'à' + directors_img + 'á ')
        # print(directors_info)

        shares = aim['shares']
        # ls
        # parse_s = re.compile(r'\[{"name": "(.*?)", "type": "(.*?)", "img": "(.*?)", "amount": "(.*?)"}]').findall(shares)
        shares_info = []
        for detail in shares:
            if 'name' in detail:
                shares_name = detail['name']
            else:
                shares_name = 'null'

            if 'type' in detail:
                shares_type = detail['type']
            else:
                shares_type = 'null'

            if 'img' in detail:
                shares_img = detail['img']
            else:
                shares_img = 'null'

            if 'amount' in detail:
                shares_amount = detail['amount']
            else:
                shares_amount = 'null'
            shares_info.append(shares_name + 'à' + shares_type + 'à' + shares_img + 'à' + shares_amount + 'á')
        # print(shares_info)

        districtCode = str(aim['districtCode'])
        cid = str(aim['cid'])
        website = str(aim['website'])
        official_flag = str(aim['official_flag'])
        shidi_pic = str(aim['shidi_pic'])
        gongzhonghao = str(aim['gongzhonghao'])
        xiongzhanghao = str(aim['xiongzhanghao'])
        weibo = str(aim['weibo'])
        phoneArr = str(aim['phoneArr'])
        baozhang_flag = str(aim['baozhang_flag'])
        shidi_flag = str(aim['shidi_flag'])
        zixin_flag = str(aim['zixin_flag'])
        chengqi_flag = str(aim['chengqi_flag'])
        v_level = str(aim['v_level'])
        v_url = str(aim['v_url'])
        content = ''
        content = content.join(search_kw + 'ÿ' + entLogo + 'ÿ' + shareLogo + 'ÿ' + entName + 'ÿ' + bdCode + 'ÿ'
                               + openStatus + 'ÿ' + entType + 'ÿ' + isClaim + 'ÿ' + claimUrl
                               + 'ÿ' + benchMark + 'ÿ' + regNo + 'ÿ' + orgNo + 'ÿ' + taxNo + 'ÿ' + scope + 'ÿ'
                               + regAddr + 'ÿ' + legalPerson + 'ÿ' + startDate + 'ÿ' + openTime + 'ÿ' + annualDate
                               + 'ÿ' + regCapital + 'ÿ' + industry + 'ÿ' + telephone + 'ÿ' + district + 'ÿ'
                               + authority + 'ÿ' + realCapital + 'ÿ' + orgType + 'ÿ' + scale + 'ÿ' + str(directors_info)
                               + 'ÿ' + str(shares_info) + 'ÿ' + districtCode + 'ÿ' + cid + 'ÿ' + website + 'ÿ'
                               + official_flag + 'ÿ' + shidi_pic + 'ÿ' + gongzhonghao + 'ÿ' + xiongzhanghao + 'ÿ'
                               + weibo + 'ÿ' + phoneArr + 'ÿ' + baozhang_flag + 'ÿ' + shidi_flag + 'ÿ' + zixin_flag
                               + 'ÿ' + chengqi_flag + 'ÿ' + str(v_level) + 'ÿ' + v_url + '\n')
        # print(content)
        self.file.write(content)
        self.file.flush()
        # item = dict(item)

        return item

    def close_spider(self, spider):
        self.file.close()

