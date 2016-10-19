# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from dapnews.items import DapnewsItem
from scrapy.linkextractors import LinkExtractor
import time
import lxml.etree
import lxml.html
from stripogram import html2text, html2safehtml
from htmlmin import minify


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
            item['imageUrl'] = ''
            if not imageUrl:
                print('DAP => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request


    def parse_detail(self, response):
        item = response.meta['item']
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        htmlcontent = ''
        for p in root.xpath('//div[@class="article-content"][1]'):
            unclean_html = lxml.html.tostring(p, encoding=unicode)
            clean_html = html2safehtml(unclean_html, valid_tags=("p", "img"))
            minified_html = minify(clean_html)
            htmlcontent = minified_html

        item['htmlcontent'] = htmlcontent
        yield item
