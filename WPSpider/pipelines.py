# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv, time

class WpspiderPipeline:

    def open_spider(self,spider):

        self.t = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        self.file = open('./' + self.t + '.csv','a+',newline='',encoding='utf-8')

    def process_item(self, item, spider):

        p_title = item['p_title']
        p_price = item['p_price']
        p_category = item['p_category']
        p_tags = item['p_tags']
        p_description = item['p_description']
        p_img = item['p_img']

        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(self.file)
        csv.field_size_limit(500 * 1024 * 1024)
        with open('./' + self.t + '.csv',"r",newline="",encoding="utf-8") as f:
            reader = csv.reader(f)
            if not [row for row in reader]:
                csv_writer.writerow(
                ["post_title", "post_name", "post_content", "post_status", "sale_price", "regular_price", "visibility",
                 "stock_status", "images", "tax:product_type", "tax:product_cat", "tax:product_tag"])
                csv_writer.writerow(
                    [p_title, p_title.lower(), p_description, "publish", "", p_price, "visible", "instock", p_img,
                     "simple", p_category, p_tags])
            else:
                # 4. 写入csv文件内容
                csv_writer.writerow(
                    [p_title, p_title.lower(), p_description, "publish", "", p_price, "visible", "instock", p_img,
                     "simple", p_category, p_tags])


        return item

    def close_spider(self, spider):

        self.file.close()




