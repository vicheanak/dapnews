
BOT_NAME = 'dapnews'

SPIDER_MODULES = ['dapnews.spiders']
NEWSPIDER_MODULE = 'dapnews.spiders'

ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'dapnews.pipelines.MySQLPipeline': 2
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'helloworld'
DB_DB = 'khmergoo_sequelize'
