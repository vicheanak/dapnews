# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from dapnews.items import DapnewsItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "dapnews"
    allowed_domains = ["dap-news.com"]
    start_urls = [
    'http://dap-news.com/kh/ព័ត៌មានក្នុងប្រទេស',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)

        for h in hxs.css('div.list-article > h1'):
            item = DapnewsItem()
            item['categoryId'] = '1'

            name = h.xpath('a/text()')
            if not name:
                print('DAP => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            description = h.xpath('following-sibling::div[@class="article-content"][1]/p/text()')
            if not description:
                print('DAP => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()

            url = h.xpath("a/@href")
            if not url:
                print('DAP => [' + now + '] No url')
            else:
                item['url'] = url.extract_first()

            imageUrl = h.xpath('following-sibling::div[@class="feature-image"][1]/img/@src')
            if not imageUrl:
                print('DAP => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item


        # list_articles = hxs.xpath('//div[@class="list-article"]')
        # titles = list_articles.xpath('//div[@class="list-article"]/h1')
        # images = list_articles.xpath('//div[@class="list-article"]/feature-image')
        # contents = list_articles.xpath('//div[@class="list-article"]/article-content')


        # for i, title in enumerate(titles):
        #     item = DapnewsItem()
        #     item['categoryId'] = '1'

        #     name = titles[i].xpath('a/text()')
        #     if not name:
        #         print('DAP => [' + now + '] No title')
        #     else:
        #         item['name'] = name.extract()[0]

        #     description = contents[i].xpath('p/text()')
        #     if not description:
        #         print('DAP => [' + now + '] No description')
        #     else:
        #         item['description'] = description[1].extract()

        #     url = titles[i].xpath("a/@href")
        #     if not url:
        #         print('DAP => [' + now + '] No url')
        #     else:
        #         item['url'] = url.extract()[0]

        #     imageUrl = images[i].xpath('img/@src')
        #     if not imageUrl:
        #         print('DAP => [' + now + '] No imageUrl')
        #     else:
        #         item['imageUrl'] = imageUrl.extract()[0]

        #     yield item

        # for article in articles:
        #     item = DapnewsItem()
        #     if "ព័ត៌មានក្នុងប្រទេស" in response.url:
        #         item['categoryId'] = '1'
        #     else:
        #         item['categoryId'] = '2'
        #     text = article.xpath('h1[0][@class="articleText"]')
        #     if not text:
        #         print('KSP => [' + now + '] No Text Container')

        #     image = article.xpath('div[@class="articleImage"]')
        #     if not image:
        #         print('KSP => [' + now + '] No Image Container')

        #     name = text.xpath('h4/a/text()')
        #     if not name:
        #         print('KSP => [' + now + '] No title')
        #     else:
        #         item['name'] = name.extract()[0]

        #     description = text.xpath('p/text()')
        #     if not description:
        #         print('KSP => [' + now + '] No description')
        #     else:
        #         item['description'] = description[1].extract()

        #     url = text.xpath("h4/a/@href")
        #     if not url:
        #         print('KSP => [' + now + '] No url')
        #     else:
        #         item['url'] = url.extract()[0]

        #     imageUrl = image.xpath('a/img/@src')
        #     if not imageUrl:
        #         print('KSP => [' + now + '] No imageUrl')
        #     else:
        #         item['imageUrl'] = imageUrl.extract()[0]

        #     yield item

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        description = hxs.xpath('//div[@id="fullArticle"]/p/text()').extract()
        new_description = '';
        for node in description:
            new_description += node
        item['description'] = new_description
        image_urls = hxs.xpath('//a[@data-fancybox-group="gallery"]/img/@src').extract()
        item['imageUrl'] = image_urls
        yield item
