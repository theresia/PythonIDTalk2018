# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopedPromoItem(scrapy.Item):
    promo_title = scrapy.Field()
    promo_period = scrapy.Field()
    promo_code = scrapy.Field()
    promo_category = scrapy.Field()
    promo_detail_link = scrapy.Field()
    promo_description = scrapy.Field()
    promo_tnc = scrapy.Field()
    promo_min_transaction = scrapy.Field()