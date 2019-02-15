from scrapy import Spider
import pandas as pd
from scrap_imdb.items import *


class SpiderCrawl(Spider):
    name = 'SpiderCrawl'
    allowed_domains = ['imdb.com']

    # final data to scrap
    # data = pd.read_csv("../../../final_data_to_scrap.csv")
    # a = '00000'
    # link_array = []
    # for i in range(len(data)):
    #     link = str(data.iloc[i][2])
    #     length = 7 - len(link)
    #     to_add = a[:length]
    #     link_array.append('https://www.imdb.com/title/tt' + to_add + link)
    # start_urls = link_array

    # ml smallest small
    data = pd.read_csv("../../../final_data_to_scrap.csv")
    a = '00000'
    link_array = []
    for i in range(len(data)):
        link = str(data.iloc[i]["imdbId"])
        link = str(link).split('.')[0]
        length = 7 - len(str(link).split('.')[0])
        to_add = a[:length]
        link_array.append('https://www.imdb.com/title/tt' + to_add + str(link))
    start_urls = link_array

    def parse(self, response):
        item = MovieItem()
        item['title'] = response.xpath('//*[@class="title_wrapper"]/h1/text()').extract_first()
        item['imdb_id'] = response.xpath("//*/meta[@property='pageId']/@content").extract_first()
        item['director'] = response.xpath("//h4[contains(text(), 'Director:')]/following-sibling::a/text()").\
            extract_first()
        if not item['director']:
            item['director'] = response.xpath("//h4[contains(text(), 'Directors:')]/following-sibling::a/text()").\
                extract()
        item['image_urls'] = response.xpath("//*/div[@class='poster']/a/img/@src").extract()
        item['year_of_release'] = response.xpath('//*[@id="titleYear"]/a/text()').extract_first()
        item['synopsis'] = response.xpath('//*[@class="summary_text"]/text()').extract_first()
        item['imdb_rating'] = response.xpath('//*[@itemprop="ratingValue"]/text()').extract_first()
        item['storyline'] = response.xpath('//*[@id="titleStoryLine"]/div[1]/p/span/text()').extract_first()

        yield item














