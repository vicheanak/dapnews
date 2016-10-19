import json
import codecs
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import time

SETTINGS = get_project_settings()


class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        #Instantiate DB
        self.dbpool = adbapi.ConnectionPool ('MySQLdb',
            host=SETTINGS['DB_HOST'],
            user=SETTINGS['DB_USER'],
            passwd=SETTINGS['DB_PASSWD'],
            port=SETTINGS['DB_PORT'],
            db=SETTINGS['DB_DB'],
            charset='utf8',
            use_unicode = True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        return item

    def _insert_record(self, tx, item):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        website_id = '2'
        tx.execute("SELECT 1 FROM NewsArticles WHERE url = %s", (item['url'], ))
        ret = tx.fetchone()
        if not ret:
            result = tx.execute("""
                INSERT INTO NewsArticles(
                name,
                description,
                url,
                imageUrl,
                createdAt,
                updatedAt,
                WebsiteId,
                NewsCategoryId,
                htmlcontent)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    item['name'],
                    item['description'],
                    item['url'],
                    item['imageUrl'],
                    now,
                    now,
                    website_id,
                    item['categoryId'],
                    item['htmlcontent']
                    ))
            if result > 0:
                self.stats.inc_value('database/items_added')


