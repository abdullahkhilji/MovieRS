# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    imdb_id = scrapy.Field()
    director = scrapy.Field()
    image_urls = scrapy.Field()
    year_of_release = scrapy.Field()
    synopsis = scrapy.Field()
    imdb_rating = scrapy.Field()
    storyline = scrapy.Field()








