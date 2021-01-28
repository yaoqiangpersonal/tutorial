# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql.cursors
import pymongo

class TutorialPipeline:
    def process_item(self, item, spider):
        return item


class BuyoyoPipeline:

    db_name = 'demo'

    def __init__(self, host,  username, password):
        # super(BuyoyoPipeline,self).__init__()
        self.host = host
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MYSQL_HOST')
        username = crawler.settings.get('MYSQL_USERNAME')
        password = crawler.settings.get('MYSQL_PASSWORD')
        return cls(host=host,username = username,password = password)

    def open_spider(self, spider):
        self.id = 0
        self.database = pymysql.connect( host=self.host, port = 3306,database = self.db_name, user = self.username, password = self.password)

    def close_spider(self, spider):
        if(hasattr(self,'database') and self.database != None):
            self.database.close()

    def process_item(self, item, spider):
        try:
            cursor = self.database.cursor()
            sql = " insert into user values(%s,%s,%s)"
            params = [item["id"],item["name"], item["price"]]
            cursor.execute(sql, params)
            self.database.commit()
        except Exception as e:
            print(e)
            self.database.rollback()

        return item


class MongoPipeline:
    
    collection_name = 'buyoyo'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item