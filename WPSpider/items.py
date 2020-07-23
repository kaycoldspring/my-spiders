# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WpspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_title = scrapy.Field()
    p_price = scrapy.Field()
    p_category = scrapy.Field()
    p_tags = scrapy.Field()
    p_description = scrapy.Field()
    p_img = scrapy.Field()


