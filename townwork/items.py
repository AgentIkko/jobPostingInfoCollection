# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# div class='jobsearch-SerpJobCard ...' 部分一致。ページに15個ほど。
# 下記すべての項目が取れるわけではない

class TownworkItem(scrapy.Item):
    # define the fields for your item here like:
    
    # 検索結果ページにだいたいある項目
    today = scrapy.Field()        # 検索日
    company = scrapy.Field() 
    tel = scrapy.Field() 
    occupation = scrapy.Field() 
    title = scrapy.Field() 
    subtitle = scrapy.Field()
    location = scrapy.Field() 
    url = scrapy.Field()
    timelimit = scrapy.Field()
    catch = scrapy.Field()
    lead = scrapy.Field()
    station = scrapy.Field()
    salary = scrapy.Field()
    workingtime = scrapy.Field()
    salaryNumHour = scrapy.Field()
    salaryNumMonth = scrapy.Field()
