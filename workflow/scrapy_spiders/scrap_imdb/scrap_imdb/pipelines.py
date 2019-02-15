# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class ScrapImdbPipeline(ImagesPipeline):
    def set_filename(self, response):
        return'full/{0}.jpg'.format(response.meta['imdb_id'])

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'imdb_id': item['imdb_id']})

    def get_images(self, response, request, info):
        for key, image, buffer in super(ScrapImdbPipeline, self).get_images(response, request, info):
            key = self.set_filename(response)
        yield key, image, buffer


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

