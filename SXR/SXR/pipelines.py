# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class SxrPipeline(object):

    def open_spider(self, spider):
        self.file = open('sxr.json', 'w+')

    def process_item(self, item, spider):
        dict_data = dict(item)
        # 转成json
        str_data = json.dumps(dict_data, ensure_ascii=False) + '\n'
        # 写入文件
        self.file.write(str_data)
        return item

    def close_spider(self, spider):
        self.file.close()
