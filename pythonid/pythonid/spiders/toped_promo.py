# -*- coding: utf-8 -*-

import scrapy
from pythonid.items import TopedPromoItem

class TopedPromoSpider(scrapy.Spider):
    name = "toped_promo"
    allowed_domains = ["tokopedia.com"]
    start_urls = ['https://www.tokopedia.com/promo/']

    def parse(self, response):
        promos = response.xpath('//div[@data-promo-title]')
        for promo in promos:
            promo_detail_link = promo.xpath(
                './/div[@class="promotion-cta"]/a/@href').extract_first()
            
            item = TopedPromoItem()
            item['promo_title'] = promo.xpath(
                './/div[@class="promotion-description"]/p/text()').extract_first()
            item['promo_period'] = promo.xpath(
                './/div[@class="promotion-box__value"]//text()').extract_first()
            item['promo_code'] = promo.xpath(
                './/input[@class="sticky-code-voucher__text"]/@value').extract_first()
            item['promo_category'] = promo.xpath('@data-promo-category').extract_first()
            item['promo_detail_link'] = promo_detail_link
            
            yield scrapy.Request(promo_detail_link, 
                callback=self.parse_promo_detail, meta={'item': item})
        
        '''
        Juga proses kategori selain Belanja (default), 
        misal Pembayaran & Top Up, Produk Keuangan
        '''
        promo_categories = response.xpath(
            '//a[contains(@class, "cat-list__item")]/@href').extract()
        for promo_category_link in promo_categories:
            yield scrapy.Request(response.urljoin(promo_category_link))

    def parse_promo_detail(self, response):
        item = response.meta.get('item')
        
        item['promo_description'] = response.xpath(
            '//div[h2[contains(@class, "post-content__heading")] and '
                '@class="post-content"]/p/text()').extract()
        item['promo_tnc'] = ''.join([s.strip() for s in response.xpath(
            '//div[@class="post-content__p"]/node()').extract() if s.strip()])
        item['promo_min_transaction'] = response.xpath(
            '//div[contains(@class, "postbox-content--min-transaction")]'
            '/p[@class="postbox-content__p"]/text()').extract_first()
        
        yield item